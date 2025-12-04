from encrypted_model_fields.fields import EncryptedCharField
from django.db import models

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    complete_name = models.CharField(max_length=255)
    password = EncryptedCharField(max_length=128)

    def __str__(self):
        return self.username

class Marketer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cellphone = EncryptedCharField(max_length=20)

    def __str__(self):
        return self.user.username

    
class Avaliation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marketplace = models.ForeignKey("marketplace.MarketPlace", on_delete=models.CASCADE)
    grade = models.IntegerField()
    comment = models.TextField()


class SiteAccess(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = "Acesso ao Site"
        verbose_name_plural = "Acessos ao Site"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"

    @classmethod
    def get_unique_visitors_count(cls):
        return cls.objects.values('ip_address').distinct().count()

    @classmethod
    def get_total_page_views(cls):
        return cls.objects.count()

    @classmethod
    def get_marketplace_visits(cls):
        return cls.objects.filter(path__startswith='/feira/').values('path').annotate(
            count=models.Count('id')
        ).order_by('-count')[:10]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey("marketplace.Products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        unique_together = [['user', 'product'], ['session_key', 'product']]

    def __str__(self):
        identifier = self.user.username if self.user else self.session_key
        return f"{identifier} - {self.product.name}"


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    search_query = models.CharField(max_length=500)
    search_type = models.CharField(max_length=50, default='geral')
    results_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historico de Pesquisa"
        verbose_name_plural = "Historico de Pesquisas"
        ordering = ['-timestamp']

    def __str__(self):
        user_info = self.user.username if self.user else self.ip_address
        return f"{user_info} - '{self.search_query}' - {self.timestamp}"

    @classmethod
    def get_top_searches(cls, limit=10):
        return cls.objects.values('search_query').annotate(
            count=models.Count('id')
        ).order_by('-count')[:limit]

    @classmethod
    def get_searches_by_type(cls):
        return cls.objects.values('search_type').annotate(
            count=models.Count('id')
        ).order_by('-count')

    @classmethod
    def get_total_searches(cls):
        return cls.objects.count()

    @classmethod
    def get_unique_searchers(cls):
        return cls.objects.values('ip_address').distinct().count()

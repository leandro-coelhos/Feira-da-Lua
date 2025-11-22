from django.db import models
from django.conf import settings


class MarketPlace(models.Model):
    name = models.CharField(max_length=255)
    marketer = models.ForeignKey(
        "marketers.Marketer",     # Marketer ainda não existe, mas Django aceita referência por string
        on_delete=models.CASCADE,
        related_name="marketplaces"
    )
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)

    # Imaginei que poderia ser campos nulos que poderiam ser atualizados dinamicamente
    average_grade = models.FloatField(null=True, blank=True)
    average_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
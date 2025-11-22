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

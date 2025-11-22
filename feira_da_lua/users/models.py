from encrypted_model_fields.fields import EncryptedCharField
from django.db import models

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    complete_name = models.CharField(max_length=255)
    password = EncryptedCharField(max_length=128)

    def __str__(self):
        return self.username
    
    def __init__(self, email, username, password, complete_name):
        self.email = email
        self.username = username
        self.password = password
        self.complete_name = complete_name

class Marketer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cellphone = EncryptedCharField(max_length=20)

    def __str__(self):
        return self.user.username
    
    def __init__(self, user, cellphone):
        self.user = user
        self.cellphone = cellphone
    
class Avaliation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marketplace = models.ForeignKey("marketplace.MarketPlace", on_delete=models.CASCADE)
    grade = models.IntegerField()
    comment = models.TextField()

    def __init__(self, user, marketplace, grade, comment):
        self.user = user
        self.marketplace = marketplace
        self.grade = grade
        self.comment = comment
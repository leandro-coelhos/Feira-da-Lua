from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    complete_name = models.CharField(max_length=255)

    # Campos padrões do AbstractUser já incluem:
    # username, email, password, first_name, last_name, etc.
    # Você pode remover first_name e last_name no settings se quiser.

    def __str__(self):
        return self.username
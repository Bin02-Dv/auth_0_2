from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class AuthApiModel(AbstractUser):
    name = models.CharField(max_length=225)
    email = models.CharField(max_length=225, unique=True)
    username = None
    password = models.CharField(max_length=225)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class APIKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(AuthApiModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.key)

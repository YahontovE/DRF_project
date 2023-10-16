from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

NULLABLE = {
    'blank': True,
    'null': True
}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=40, verbose_name='город')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

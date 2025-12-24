from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    joined_products = models.ManyToManyField('deposits.DepositProduct', blank=True, related_name='users_joined')

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
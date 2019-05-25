from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import Basket


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
        
    def save(self, *args, **kwargs):
        is_new = False if self.id else True
        super(CustomUser, self).save(*args, **kwargs)
        if is_new:
            basket = Basket()
            basket.user = self
            basket.save()

    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.apps import apps


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    basket = models.OneToOneField(to='core.Basket', on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        is_new = False if self.id else True
        super(CustomUser, self).save(*args, **kwargs)
        if is_new:
            print('ALLERT!')
            Basket = apps.get_model('core', 'Basket')
            basket = Basket()
            basket.save()
            self.basket = basket


    def __str__(self):
        return self.email

from django.db import models
from django.contrib.postgres.fields import JSONField



class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta():
        verbose_name_plural = "categories"


class Product(models.Model):
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    manufacturer = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    general_info = models.TextField(blank=True)
    release_date = models.DateField(blank=True)
    specifications = JSONField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)


class Basket(models.Model):
    products = models.ManyToManyField(to=Product)
    

class Order(models.Model):
    RECIEVED = 0
    PROCCESSED = 1
    DELIVERED = 2
    REJECTED = 3
    
    STATUSES = (
        (RECIEVED, 'RECIEVED'),
        (PROCCESSED, 'PROCCESSED'),
        (DELIVERED, 'DELIVERED'),
        (RECIEVED, 'REJECTED'),
    )

    products = models.ManyToManyField(to=Product)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=RECIEVED)
    user = models.ForeignKey(to='user.CustomUser', on_delete=models.CASCADE)



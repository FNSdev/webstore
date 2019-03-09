from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta():
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=40, default="")
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    manufacturer = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    general_info = models.TextField(blank=True)
    release_date = models.DateField(blank=True)
    specifications = JSONField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='products')
    view_count = models.IntegerField(default=0)
    image = models.ImageField(blank=True)

    class Meta:
        ordering = ('view_count', 'name')

    def __str__(self):
        return f'{self.name}'


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



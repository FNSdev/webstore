from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.text import slugify

from uuid import uuid4
import time

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True)

    def save(self, *args, **kwargs):
        old = Category.objects.filter(slug__iexact=self.slug).first()
        if old:
            if old.name!=self.name:
                self.slug = slugify(f'{self.name}-{int(time.time())}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta():
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=40, default="")
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    general_info = models.TextField(blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='products')
    specifications = HStoreField(blank=True, default=dict)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        old = Product.objects.filter(slug__iexact=self.slug).first()
        if old:
            if old.name!=self.name:
                self.slug = slugify(f'{self.name}-{int(time.time())}')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-view_count', 'name')

    def __str__(self):
        return f'{self.name}'


def product_image_upload_path(instance, filename):
    return f'{instance.product.name} / {uuid4()}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_upload_path)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url
       

class Basket(models.Model):
    products = models.ManyToManyField(to=Product, through='ProductInBasket')   
    total_count = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return f'basket of {self.customuser.email}'


class ProductInBasket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(to=Basket, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} in "{self.basket.customuser.email}" basket'
    

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


def announcement_image_upload_path(instance, filename):
    return f'{instance.header} / {uuid4()}'


class Announcement(models.Model):
    header = models.CharField(max_length=80)
    body = models.TextField()
    slug = models.SlugField(blank = True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to=announcement_image_upload_path)

    class Meta:
        ordering = ('-date', )

    def save(self, *args, **kwargs):
        old = Announcement.objects.filter(slug__iexact=self.slug).first()
        if old:
            if old.header!=self.header:
                self.slug = slugify(f'{self.header}-{int(time.time())}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.header



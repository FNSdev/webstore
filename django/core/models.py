from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.text import slugify
from django.core.validators import MaxValueValidator


from uuid import uuid4
import time

MAX_PRODUCT_IN_BASKET_OR_ORDER_COUNT = 10

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True)
    specifications = HStoreField(default=dict)

    def save(self, *args, **kwargs):
        from core.forms import FormGenerator, GENERATED_FORMS
        old = Category.objects.filter(slug__iexact=self.slug).first()
        if old:
            if old.name != self.name:
                self.slug = slugify(f'{self.name}-{int(time.time())}')
            if old.name != self.name or old.specifications != self.specifications:
                form = FormGenerator.generate(self.slug, self.specifications)
                GENERATED_FORMS[self.slug] = form
        else:  
            self.slug = slugify(f'{self.name}-{int(time.time())}')          
            form = FormGenerator.generate(self.slug, self.specifications)
            GENERATED_FORMS[self.slug] = form
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
    slug = models.SlugField(blank=True)
    user_reviews = models.ManyToManyField(to='user.CustomUser', through='Review')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        old = Product.objects.filter(slug__iexact=self.slug).first()
        if old:
            if old.name!=self.name:
                self.slug = slugify(f'{self.name}-{int(time.time())}')
        else:
            self.slug = slugify(f'{self.name}-{int(time.time())}')
        super().save(*args, **kwargs)

    def update_rating(self):
        reviews = Review.objects.filter(product=self)
        total = 0
        for review in reviews:
            total += (review.rating + 1)
        total = total / len(reviews)
        self.rating = total
        self.save()

    def get_stars(self):
        return self.rating * 20

    class Meta:
        ordering = ('-rating', 'name')

    def __str__(self):
        return f'{self.name}'


def product_image_upload_path(instance, filename):
    return f'{instance.product.name}/{uuid4()}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_upload_path)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url
       

class Basket(models.Model):
    products = models.ManyToManyField(to=Product, through='ProductInBasket')   
    total_count = models.PositiveIntegerField(default=0)
    coupone_code = models.UUIDField(null=True, blank=True)
    user = models.OneToOneField(to='user.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    def get_total_price(self):
        total = 0
        products = ProductInBasket.objects.filter(basket=self)
        for product in products.all():
            total += product.product.price * product.count
        return total

    """def __str__(self):
        return f'basket of {self.user.email}'"""


class Coupone(models.Model):
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    code = models.UUIDField(default=uuid4, editable=False)


class ProductInBasket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(to=Basket, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price * int(self.count)

    def __str__(self):
        return f'{self.product.name} in the "{self.basket}'
    

class Order(models.Model):
    RECIEVED = 0
    PROCCESSED = 1
    DELIVERED = 2
    REJECTED = 3
    
    STATUSES = (
        (RECIEVED, 'RECIEVED'),
        (PROCCESSED, 'PROCCESSED'),
        (DELIVERED, 'DELIVERED'),
        (REJECTED, 'REJECTED'),
    )

    products = models.ManyToManyField(to=Product, through='ProductInOrder')
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=RECIEVED)    
    user = models.ForeignKey(to='user.CustomUser', on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    price_with_discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    class Meta:
        ordering = ('-date', '-total_price')

    def __str__(self):
        return f'order of {self.user.email}, {self.date}'


class ProductInOrder(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price * int(self.count)

    def __str__(self):
        return f'{self.product.name} in the {self.order}'


def announcement_image_upload_path(instance, filename):
    return f'{instance.header}/{uuid4()}'


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
        else:
            self.slug = slugify(f'{self.header}-{int(time.time())}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.header


class ReviewManager(models.Manager):
    def get_review_or_unsaved_blank_review(self, product, user):
        try:
            return Review.objects.get(product=product, user=user)
        except Review.DoesNotExist:
            return Review(product=product, user=user)


class Review(models.Model):
    VERY_BAD = 0
    BAD = 1
    FINE = 2
    GOOD = 3
    AWESOME = 4

    RATINGS = (
        (VERY_BAD, 'Very Bad'),
        (BAD, 'Bad'),
        (FINE, 'Fine'),
        (GOOD, 'Good'),
        (AWESOME, 'Awesome'),
    )

    class Meta():
        ordering = ('-date',)
        unique_together = ('user', 'product')

    objects = ReviewManager()

    user = models.ForeignKey(to='user.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, default=FINE)
    header = models.CharField(max_length=60)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review of {self.product.name} from {self.user.username}'
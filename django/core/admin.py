from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['slug']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['slug']

class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    readonly_fields = ['slug']
    

admin.site.register(Basket)
admin.site.register(ProductInBasket)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductInOrder)

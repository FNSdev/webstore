from django.contrib import admin

from core.models import *


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['slug']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['slug']

class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    readonly_fields = ['slug']

class CouponeAdmin(admin.ModelAdmin):
    model = Coupone
    readonly_fields = ['code']
    

admin.site.register(Basket)
admin.site.register(ProductInBasket)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductInOrder)
admin.site.register(Review)
admin.site.register(Coupone, CouponeAdmin)
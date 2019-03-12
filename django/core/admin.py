from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fields = ['name', 'slug']
    readonly_fields = ['slug']
    list_display = ['name']


admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Announcement)
admin.site.register(Category, CategoryAdmin)

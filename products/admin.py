from django.contrib import admin

from products.models import Category, Product, MinimumOrderQuantity, Unit

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(MinimumOrderQuantity)
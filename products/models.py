from django.db import models

from suppliers.models import Company


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    root = models.ForeignKey('Category', blank=True, null=True, on_delete=models.BLANK_CHOICE_DASH)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'category'


class Unit(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'unit'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, blank=True, null=True, on_delete=models.BLANK_CHOICE_DASH)
    start_price = models.PositiveIntegerField()
    end_price = models.PositiveIntegerField()

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'product'


class MinimumOrderQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'MOQ: {self.product.name} {self.quantity} {self.product.unit.name} {self.description}'

    class Meta:
        db_table = 'minimum_order_quantity'

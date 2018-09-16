from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics

from products.models import Category, Product


class PayloaderMixin(object):
    payloads = {'results': None, 'meta': {}, 'links': {'next': '', 'prev': ''}}

class RecursiveCategoryMixin(object):
    def _recursive(self, obj):
        childs = self.model.objects.filter(root=obj)
        data = []
        for child in childs:
            if self._have_child(child):
                data.append({
                    'title': child.name,
                    'key': child.slug,
                    'children': self._recursive(child)
                })
            else:
                data.append({
                    'title': child.name,
                    'key': child.slug
                })

        return data

    def _have_child(self, obj):
        return self.model.objects.filter(root=obj)


class CategoryListView(View, PayloaderMixin, RecursiveCategoryMixin):
    model = Category

    def get(self, request):
        self.payloads['results'] = []
        categories = Category.objects.filter(root=None)
        for category in categories:
            if self._have_child(category):
                self.payloads['results'].append({
                    'title': category.name,
                    'key': category.slug,
                    'children': self._recursive(category)
                })
            else:
                self.payloads['results'].append({
                    'title': category.name,
                    'key': category.slug
                })

        return JsonResponse(self.payloads, safe=False, status=200)


class ProductListView(View, PayloaderMixin, RecursiveCategoryMixin):
    def get(self, request, category_slug=None):
        self.payloads['results'] = []
        q = request.GET.get('q', None)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category__in=[category], company__is_active=True)
        else:
            products = Product.objects.filter(company__is_active=True)

        if q:
            products = products.filter(name__icontains=q)

        for product in products:
            moq = product.minimumorderquantity_set.first()
            self.payloads['results'].append({
                'name': product.name,
                'slug': product.slug,
                'category': [{
                    'title': obj.name,
                    'key': obj.slug
                } for obj in product.category.all()],
                'company': {
                    'owner': product.company.owner.username,
                    'name': product.company.name,
                    'slug': product.company.slug,
                    'is_active': product.company.is_active
                },
                'unit': {
                    'code': product.unit.code,
                    'name': product.unit.name
                },
                'start_price': product.start_price,
                'end_price': product.end_price,
                'moq': f'{moq.quantity} / {product.unit.name} {moq.description}'
            })

        return JsonResponse(self.payloads, safe=False, status=200)


class ProductDetailView(View, PayloaderMixin, RecursiveCategoryMixin):
    def get(self, request, product_slug, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, slug=product_slug, category__in=[category])
        moq = product.minimumorderquantity_set.first()

        self.payloads['results'] = {
            'name': product.name,
            'slug': product.slug,
            'category': [{
                'title': obj.name,
                'key': obj.slug
            } for obj in product.category.all()],
            'company': {
                'owner': product.company.owner.username,
                'name': product.company.name,
                'slug': product.company.slug,
                'is_active': product.company.is_active
            },
            'unit': {
                'code': product.unit.code,
                'name': product.unit.name
            },
            'start_price': product.start_price,
            'end_price': product.end_price,
            'moq': f'{moq.quantity} / {product.unit.name} {moq.description}'
        }

        return JsonResponse(self.payloads, safe=False, status=200)
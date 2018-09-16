from django.urls import path, re_path

from products import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    re_path(r'^products/?(?P<category_slug>\w+)?/?$', views.ProductListView.as_view()),
    path('products/<slug:product_slug>/<slug:category_slug>/', views.ProductDetailView.as_view())
]
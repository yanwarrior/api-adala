from django.urls import path

from products import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('products/<slug:category_slug>/', views.ProductListView.as_view()),
    path('products/<slug:product_slug>/<slug:category_slug>/', views.ProductDetailView.as_view())
]
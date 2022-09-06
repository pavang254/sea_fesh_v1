from django.urls import path
from .views import home, product_detail, update_cart, category_detail

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:name>/', category_detail, name='category_detail'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', update_cart, name='cart'),
]
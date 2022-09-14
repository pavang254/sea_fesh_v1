from django.urls import path
from .views import home, product_detail, cart, category_detail, checkout, process_order, orderItems

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:name>/', category_detail, name='category_detail'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('process_order/',process_order, name='process_order'),
    path('orderItems/<int:id>',orderItems, name='orderItems'),
]
import json
from unicodedata import category
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Catgegory
# Create your views here.

def home(request):
    products = Product.objects.all()
    categories = Catgegory.objects.all()[:3]
    context = {"products":products, "categories":categories}

    return render(request, 'app_v1/home.html', context)

def category_detail(request, name):
    return JsonResponse({'category:':name})

def product_detail(request, slug):
    product = Product.objects.get(product_slug=slug)

    return render(request, 'app_v1/product.html', {"product":product})

def update_cart(request):
    if request.method == 'POST':
        cart = json.loads(request.body)
        cart = cart['basket']
        
        for item in cart:
            if Product.objects.get(name = item['name']):
               print(Product.price) 

        return JsonResponse({'items':len(cart)})
    return render(request, 'app_v1/cart.html')
from copyreg import constructor
import decimal
import json
from venv import create
from django.shortcuts import render
from django.http import JsonResponse

from .models import Customer, Order, Product, Catgegory, OrderItem
from .utils import guestCartCookie, userCheckout

# Create your views here.

def home(request):
    try:
        cookieData = guestCartCookie(request)
        cartItems = cookieData['cartItems']
    except:
        cartItems = 0

    products = Product.objects.all()
    categories = Catgegory.objects.all()[:3]

    context = {'products':products, 'categories':categories, 'cartItems':cartItems}
    return render(request, 'app_v1/home.html', context)

def category_detail(request, name):
    products = Product.objects.get(category__cat_name=name)
    print(products)
    return JsonResponse({'category:':name})

def product_detail(request, slug):
    product = Product.objects.get(product_slug=slug)

    try:
        cookieData = guestCartCookie(request)
        cartItems = cookieData['cartItems']
    except:
        cartItems = 0

    context = {'product':product,  'cartItems':cartItems}
    return render(request, 'app_v1/product.html', context)

def cart(request):
    try:
        cookieData = guestCartCookie(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    except:
        return JsonResponse('product you tried to add may have gone out of stock', safe=False)

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'app_v1/cart2.html',context)

""" 
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    product = Product.objects.get(id=productId)
    order, _ = Order.objects.get_or_create(order_complete=False)

    return JsonResponse('cart item updated', safe=False)
"""

def checkout(request):
    try:
        cookieData = guestCartCookie(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    except:
        return JsonResponse('product you tried to add may have gone out of stock', safe=False)

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'app_v1/checkout.html', context)

def process_order(request):
    data = json.loads(request.body)
    total = float(data['form']['total'])
    
    customer, order = userCheckout(request, data)

    print('new order created with id= ', order.id)
    print('total in process order= ',order.get_cart_total)
    print('total from req body= ',total)
    if total == order.get_cart_total:
        order.order_complete = True
    order.save()

    print('order received with id= ', order.id)
    print('customer details: ', customer.phone_number, customer.shipping_address)
    print('order details: ', order.id, order.payment_mode)

    orderItems = OrderItem.objects.filter(order=order.id)
    try:
        for item in orderItems:
            print(f'name: {item.product.name}, quantity= {item.quantity}')
    except:
        print(f'name: {orderItems.product.name}, quantity= {orderItems.quantity}')
    
    return JsonResponse('order received, wait for further updates', safe=False)

def orderItems(request, id):
    items = OrderItem.objects.filter(order_id=id)
    
    a = [item.product.name for item in items ]
    q = [float(item.quantity) for item in items ]

    products = zip(a, q)
    products=dict(products)
    data = {'product':products}

    return JsonResponse(data, safe=False)

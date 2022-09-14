import datetime
import decimal
import json
from .models import Order, Product, OrderItem, Customer

def guestCartCookie(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print('cart: ', cart)
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items'] 

    for i in cart:
        try:
            cartItems += float(cart[i]['quantity'])

            product = Product.objects.get(id=i)
            total = float(product.price * decimal.Decimal(cart[i]['quantity']))

            print('total= ',total)
            print('quantity= ',float(cart[i]['quantity']))

            order['get_cart_total'] += total
            order['get_cart_items'] +=1

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':float(cart[i]['quantity']),
                'get_total':total,
            }
            items.append(item)
        except:
            pass

    return {'order':order, 'items':items, 'cartItems':cartItems}


def userCheckout(request, data):
    transaction_id = datetime.datetime.now().timestamp()

    name = data['form']['name']
    phone = data['form']['phone']
    address = data['form']['address']
    payment = data['form']['payment']

    cookieData = guestCartCookie(request)
    items = cookieData['items']
    print('items in user checkout: ',items)

    customer, _ = Customer.objects.get_or_create(phone_number = phone)
    customer.name = name
    customer.shipping_address = address
    customer.save()

    order = Order.objects.create(customer=customer, payment_mode=payment, order_complete=False)
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])
        print(f'order item created with qty={orderItem.quantity} for product {orderItem.product.name} on order-id={orderItem.order.id}')

    return customer, order
from django.utils.text import slugify
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class Catgegory(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=10)
    cat_image = models.ImageField(null=True, blank=True, upload_to = 'images/')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.cat_name


class Product(models.Model):
    SIZE =[
        ('SMALL', 'Small'),
        ('MEDIUM', 'Med'),
        ('BIG', 'Big'),
        ('WHOLE', 'Whole'),
    ]

    name = models.CharField(max_length=100)
    product_slug = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey(Catgegory, default='Fish', on_delete=models.SET_DEFAULT)
    size = models.CharField(max_length=20, choices=SIZE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to = 'images/')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.product_slug = "%s_%s" % (self.category.cat_name , slugify(self.name))
        return super().save(*args, **kwargs)
    

class FreshCatch(models.Model):
    name = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    fresh_image = models.ImageField(null=True, blank=True, upload_to='fresh_catch/%Y.%m.%d')

    class Meta:
        verbose_name_plural = 'fresh_catches'

    def __str__(self) -> str:
        return f'{self.name.name}_{self.date_added}'


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField()
    mail = models.EmailField(blank=True, null=True)
    shipping_address = models.CharField(max_length=200, db_column='Shipping_Address')
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.phone_number)

class Order(models.Model):
    ORDER_STATUS =[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('OUT_FOR_DELIVERY', 'Out for delivery'),
        ('DELIVERED', 'Delivered'),
    ]

    PAYMENT_MODE = [
        ('UPI', 'Upi'),
        ('CASH_ON_DELIVERY', 'COD'),
    ]

    PAID = [
        ('YES', 'yes'),
        ('PENDING', 'no'),
    ]

    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    order_date = models.DateTimeField(auto_now_add=True, db_column='Order_date')
    order_complete = models.BooleanField(default=False) #if false can continue to add items to same cart
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, default='CASH_ON_DELIVERY')
    paid = models.CharField(max_length=10, choices=PAID, default='PENDING')
    
    def __str__(self) -> str:
        return str(self.id)

    @property
    def get_cart_total(self):   #total value of the cart
        orderitems =  self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):   #total number of items in cart
        order_items =  self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.order.order_id

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
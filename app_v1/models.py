from itertools import product
from statistics import mode
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
# Create your models here.

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
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to = 'images/')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.product_slug = "%s_%s" % (self.category.cat_name , slugify(self.name))
        return super().save(*args, **kwargs)
    

class Fresh_Catch(models.Model):
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
    order_status = models.CharField(choices=ORDER_STATUS, default='Pending')
    payment_mode = models.CharField(choices=PAYMENT_MODE, default='COD')
    paid = models.CharField(choices=PAID, default='no')
    
    def __str__(self) -> str:
        return str(self.id)

class Order_Item(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name

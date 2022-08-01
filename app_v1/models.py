from statistics import mode
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.

fs = FileSystemStorage(location='/media/photos')

class Catgegory(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.cat_name

class Product(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Catgegory, default='Fish', on_delete=models.SET_DEFAULT)
    image = models.ImageField(storage=fs, null=True)

    def __str__(self) -> str:
        return self.name
    
class Size_Price(models.Model):
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE) 
    small_price = models.FloatField()
    med_price = models.FloatField()
    big_price = models.FloatField()

    def __str__(self) -> str:
        return f' {self.prod_id} -> small = {self.small_price}, med = {self.med_price}, big = {self.big_price} '

class Prod_details(models.Model):
    type_clean = models.BooleanField(default=True)
    price = models.ForeignKey(Size_Price, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.price



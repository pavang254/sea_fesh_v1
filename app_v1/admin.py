from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Catgegory)
admin.site.register(Product)
admin.site.register(Size_Price)
admin.site.register(Prod_details)
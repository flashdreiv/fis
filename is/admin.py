from django.contrib import admin
from . models import Farmer,Product,Purchase
# Register your models here.

admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Purchase)
from django.contrib import admin
from . models import Farmer,Product,Coupon,SalesLady,Purchase,Province,Municipality
# Register your models here.

admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(SalesLady)
admin.site.register(Purchase)
admin.site.register(Province)
admin.site.register(Municipality)

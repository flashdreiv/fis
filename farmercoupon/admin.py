from django.contrib import admin
from accounts.models import Farmer,SalesLady
from farmercoupon.models import Product,Coupon,Purchase
# Register your models here.

admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(SalesLady)
admin.site.register(Purchase)



from django.db import models
from django.conf import settings
from accounts.models import Farmer,SalesLady
from ph_locations.models import Region,Province,City,Barangay
from multiselectfield import MultiSelectField
from django.core.exceptions import PermissionDenied
from . generate_random_coupon import generate_coupon_code
# Create your models here.
class Product(models.Model):
    category = (
        ('1','Y+ Package'),
        ('2','Aljay Biotech'),
        ('3','Premium Grade Fertilizers'),
        ('4','Aljay Hybrid Seed'),
        ('5','Fungicide'),
        ('6','Herbicide'),
        ('7','Insecticide'),
        ('8','Molluscicide'),
        ('9','Foliar Fertilizers'),
    )
    item_name = models.CharField(max_length=50)
    item_category = models.CharField(max_length=50,choices=category,null=True)
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    ticket_value = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name

class Coupon(models.Model):
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    ticket_value = models.IntegerField(default=0)
    farmer = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.SET_NULL,null=True,blank=True)
    code = models.CharField(max_length=20,unique=True,default=0)
    is_golden_ticket=models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    purchase_date = models.DateField(null=True,blank=True)
    generate_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.farmer is None:
            self.code = generate_coupon_code('ALJAY-') 
        elif self.item:
            if int(self.item.item_category) == 1:
                self.is_golden_ticket = True
        

        super(Coupon, self).save(*args, **kwargs)

        # else:
        #     if int(self.item.item_category) == 1:
        #         self.is_golden_ticket = True
        #         self.farmer.golden_ticket +=1
        #         self.saleslady.golden_ticket +=1
        #     elif int(self.item.item_category) > 1:
        #         self.farmer.standard_ticket +=1
        #         self.saleslady.standard_ticket +=1
        #     self.farmer.save()
        #     self.saleslady.save()
        #     try:
        #         self.code = generate_coupon_code('Generated-')
        #     except:
        #         raise PermissionDenied
        

class Purchase(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_now=True)
    purchase_date = models.DateField(null=True,blank=True)
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)

        


    







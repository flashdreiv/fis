from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Farmer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    province = models.ForeignKey(Province,on_delete=models.SET_NULL,blank=True,null=True)
    municipality = models.ForeignKey(Municipality,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return self.user.first_name

class SalesLady(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=15)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.first_name

class Product(models.Model):
    category = (
        ('1','Y+ Package'),
        ('2','Aljay Seeds'),
        ('3','Aljay Chemicals'),
        ('4','Aljay Fertilizer')
    )
    item_name = models.CharField(max_length=50)
    ticket_value = models.IntegerField(default=0)
    item_category = models.CharField(max_length=50,choices=category,null=True)
    price = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.item_name

class Coupon(models.Model):
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.SET_NULL,null=True,blank=True)
    code = models.CharField(max_length=15,unique=True,default=0)
    is_golden_ticket=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

#Check SAP Data on Purchase Orders
class Purchase(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.SET_NULL,null=True,blank=True)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    purchase_date = models.DateTimeField(auto_now=True)




    







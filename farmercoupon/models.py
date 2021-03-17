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
    is_blo = models.BooleanField(default=False)
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
    def __str__(self):
        return self.item_name

class Coupon(models.Model):
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    ticket_value = models.IntegerField(default=0)
    farmer = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.SET_NULL,null=True,blank=True)
    code = models.CharField(max_length=15,unique=True,default=0)
    is_golden_ticket=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    purchase_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.code





    







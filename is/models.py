from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Farmer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.first_name

class SalesLady(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.first_name

class Product(models.Model):
    category = (
        ('Aljay Chemicals','Aljay Chemicals'),
        ('Allied Chemicals','Allied Chemicals'),
        ('Fertilizer','Fertilizer')
    )
    item_name = models.CharField(max_length=50)
    ticket_value = models.IntegerField(default=0)
    item_category = models.CharField(max_length=50,choices=category,null=True)
    is_active = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)
    def __str__(self):
        return self.item_name

# class Purchase(models.Model):
#     purchase_date = models.DateTimeField(auto_now=True)
#     item = models.ForeignKey(Product,on_delete=models.CASCADE)
#     def __str__(self):
#         return self.item

class Coupon(models.Model):
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True,blank=True)
    saleslady = models.ForeignKey(SalesLady,on_delete=models.SET_NULL,null=True,blank=True)
    code = models.CharField(max_length=15,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    







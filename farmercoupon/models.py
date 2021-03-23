from django.db import models
from django.contrib.auth.models import User,Group
from ph_locations.models import Region,Province,City,Barangay
from multiselectfield import MultiSelectField
# Create your models here.


class Farmer(models.Model):
    CROP_LIST = ((1, 'RICE'),
               (2, 'CORN'),
               (3, 'VEGETABLES'),
               (4, 'FRUITS'),
               (5, 'ORNAMENTALS'),
               )
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=13,null=True,blank=True,unique=True)
    access_token = models.CharField(max_length=100,null=True,blank=True,unique=True)
    globe_code = models.CharField(max_length=500,null=True,blank=True,unique=True)
    land_area = models.IntegerField(default=0)
    crops = MultiSelectField(choices=CROP_LIST,blank=True,null=True)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    region = models.ForeignKey(Region,on_delete=models.SET_NULL,null=True)
    province = models.ForeignKey(Province,on_delete=models.SET_NULL,null=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True)
    barangay = models.ForeignKey(Barangay,on_delete=models.SET_NULL,null=True,blank=True)
    groups = models.ForeignKey(Group,null=True,on_delete=models.CASCADE)

    def save(self, *args, **kwargs): 
        #Group must be farmer
       self.groups = Group.objects.get(pk=2)
       super(Farmer, self).save(*args, **kwargs) 
       
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class SalesLady(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=13,null=True,blank=True,unique=True)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    is_new_user = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

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
    code = models.CharField(max_length=15,unique=True,default=0)
    is_golden_ticket=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    purchase_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.code





    







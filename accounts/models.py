from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from ph_locations.models import Region,Province,City,Barangay

# Create your models here.

class Farmer(models.Model):
    CROP_LIST = ((1, 'RICE'),
               (2, 'CORN'),
               (3, 'VEGETABLES'),
               (4, 'FRUITS'),
               (5, 'ORNAMENTALS'),
               )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
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
    is_new_user = models.BooleanField(default=True)

       
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class SalesLady(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=13,null=True,blank=True,unique=True)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    is_new_user = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

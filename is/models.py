from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Farmer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    standard_ticket = models.IntegerField(default=0)
    golden_ticket = models.IntegerField(default=0)
    
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

    def __str__(self):
        return self.item_name

class Purchase(models.Model):
    purchase_date = models.DateTimeField(auto_now=True)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.item






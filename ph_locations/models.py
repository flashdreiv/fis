from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=80,null=True)
    
    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=80,null=True)
    region = models.ForeignKey(Region,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=80,null=True)
    province = models.ForeignKey(Province,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

class Barangay(models.Model):
    name = models.CharField(max_length=80,null=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name




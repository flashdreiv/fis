from django import forms
from django.contrib.auth.models import User
from . models import Farmer
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class YFarmerForm(UserCreationForm):
    provinces = (
        ('Isabela','Isabela'),
        ('NCR','NCR'),
        ('Calabarzon','Calabarzon')
    )
    location = forms.ChoiceField(choices=provinces)
    mobile_number = forms.CharField(max_length=12)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','location','mobile_number']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

class ApplyCouponForm(forms.Form):
    code = forms.CharField(required=False)
    
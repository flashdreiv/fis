from django import forms
from django.contrib.auth.models import User,Group
from . models import Farmer,Coupon,Product,SalesLady,Province,Municipality
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
    saleslady_list = [
        (saleslady.pk,saleslady.user.first_name + ' '+saleslady.user.last_name) for saleslady in SalesLady.objects.all()
    ]
    code = forms.CharField(required=True)
    saleslady = forms.ChoiceField(required=True,choices=saleslady_list)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit Coupon', css_class='btn-primary'))

class GenerateCouponForm(forms.Form):
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Generate Coupon', css_class='btn-primary'))
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)')
    item = forms.ChoiceField(choices=product_list,label="Item for coupon")

class SalesReportForm(forms.Form):
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    province_list = [
        (province.pk,province.name) for province in Province.objects.all()
    ]
    dateFrom = forms.DateField(required=True)
    dateTo = forms.DateField(required=True)
    province = forms.ChoiceField(choices=province_list,required=True)
    item = forms.ChoiceField(choices=product_list,required=True)
    







    
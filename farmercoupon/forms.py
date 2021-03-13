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
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    code = forms.CharField(required=True)
    saleslady = forms.ChoiceField(required=True,choices=saleslady_list)
    item = forms.ChoiceField(required=True,choices=product_list)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit Coupon', css_class='btn-primary'))

class GenerateCouponForm(forms.Form):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Generate Coupon', css_class='btn-primary'))
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)')
    ticket_value = forms.IntegerField(min_value=1,max_value=20,label='Enter ticket value',required=True)
    # item = forms.ChoiceField(choices=product_list,label="Item for coupon")

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

class ApplyCouponFormBlo(forms.Form):
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    saleslady_list = [
        (saleslady.pk,saleslady.user.first_name + ' '+saleslady.user.last_name) for saleslady in SalesLady.objects.all()
    ]
    farmer_list = [
        (farmer.pk,farmer.user.first_name + ' '+farmer.user.last_name) for farmer in Farmer.objects.filter(is_blo=True)
    ]
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Apply Coupon', css_class='btn-primary'))
    saleslady = forms.ChoiceField(required=True,choices=saleslady_list)
    farmer = forms.ChoiceField(required=True,choices=farmer_list)
    item = forms.ChoiceField(choices=product_list,required=True)
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)')
    ticket_value = forms.IntegerField(min_value=1,max_value=20,label='Enter ticket value',required=True)
    






    

from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User,Group
from . models import Farmer,SalesLady
from farmercoupon.models import Product
from ph_locations.models import Region,Province,City,Barangay

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
class ApplyCouponForm(forms.Form):
    saleslady_list = [
        (saleslady.pk,saleslady.user.first_name + ' '+ saleslady.user.last_name) for saleslady in SalesLady.objects.all()
    ]
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    code = forms.CharField(required=True)
    saleslady = forms.ChoiceField(required=True,choices=saleslady_list)
    item = forms.ChoiceField(required=True,choices=product_list)

class AddFarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['mobile_number','region','province','city','crops','land_area']
        
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        
        for field in self.fields:
            self.fields[field].required = True

        self.fields['province'].queryset = Province.objects.none()
        self.fields['city'].queryset = City.objects.none()
        if 'province' and 'city' in self.data:
            try:
                region_id = int(self.data.get('region'))
                province_id = int(self.data.get('province'))
                city_id = int(self.data.get('city'))
                self.fields['province'].queryset = Province.objects.filter(region_id=region_id).order_by('name')
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
             self.fields['province'].queryset = self.instance.region.province_set.all()
             self.fields['city'].queryset = self.instance.province.city_set.all()

class SalesLadyForm(forms.ModelForm):
    class Meta:
        model = SalesLady
        fields  = ['branch_name','mobile_number']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User

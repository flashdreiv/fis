
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User,Group
from . models import Farmer,SalesLady
from farmercoupon.models import Product,Coupon
from ph_locations.models import Region,Province,City,Barangay

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

class ApplyCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','saleslady','item']
    # code = forms.CharField(max_length=20)

    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].required = True    
class AddFarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['mobile_number','region','province','city','crops','land_area']

    def clean_land_area(self):
        land_area = self.cleaned_data.get('land_area')
        return land_area if land_area is not None else 0

    def clean_standard_ticket(self):
        standard_ticket = self.cleaned_data.get('standard_ticket')
        return standard_ticket if standard_ticket is not None else 0

    def clean_golden_ticket(self):
        golden_ticket = self.cleaned_data.get('golden_ticket')
        return golden_ticket if golden_ticket is not None else 0
        
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

from django import forms
from django.contrib.auth.models import User,Group
from . models import Farmer,Coupon,Product,SalesLady
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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

class GenerateCouponForm(forms.Form):
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)')
    ticket_value = forms.IntegerField(min_value=1,max_value=20,label='Enter ticket value',required=True)

class SalesReportForm(forms.Form):
    product_list = [
        (product.pk,product.item_name) for product in Product.objects.all()
    ]
    # province_list = [
    #     (address.pk,address.province) for address in Address.objects.all()
    # ]
    category_list = (
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
    dateFrom = forms.DateField(required=True)
    dateTo = forms.DateField(required=True)
    # province = forms.ChoiceField(choices=province_list,required=True)
    item = forms.ChoiceField(choices=product_list,required=True)
    category = forms.ChoiceField(choices=category_list,required=True)

# class ApplyCouponFormBlo(forms.Form):
#     product_list = [
#         (product.pk,product.item_name) for product in Product.objects.order_by('-item_name')
#     ]
#     saleslady_list = [
#         (saleslady.pk,saleslady.user.first_name + ' '+saleslady.user.last_name) for saleslady in SalesLady.objects.all()
#     ]
#     farmer_list = [
#         (farmer.pk,farmer.user.first_name + ' '+ farmer.user.last_name) for farmer in Farmer.objects.all()
#     ]
#     helper = FormHelper()
#     helper.add_input(Submit('submit', 'Apply Coupon', css_class='btn-primary'))
#     saleslady = forms.ChoiceField(required=True,choices=saleslady_list,label='Sales')
#     farmer = forms.ChoiceField(required=True,choices=farmer_list)
#     item = forms.ChoiceField(choices=product_list,required=True)
#     count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)',required=True)

class ApplyPurchaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(Product.objects.order_by('-item_name'))
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)',required=True)
    class Meta:
        model = Coupon
        ordering = ['item']
        fields = ['farmer','saleslady','item','purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].required = True
    
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

 
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User

    
        


        

        







    
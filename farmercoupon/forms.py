from django import forms

from accounts.models import Farmer,SalesLady
from  . models import Product,Coupon,Purchase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Button
from crispy_forms.bootstrap import FormActions




class GenerateCouponForm(forms.Form):
    count = forms.IntegerField(min_value=0,max_value=300,label='Number of coupons to generate(Max=300)')
    ticket_value = forms.IntegerField(min_value=1,max_value=20,label='Enter ticket value',required=True)

class SalesReportForm(forms.Form):
    category_list = (
        ('1', 'Y+ Package'),
        ('2', 'Aljay Biotech'),
        ('3', 'Premium Grade Fertilizers'),
        ('4', 'Aljay Hybrid Seed'),
        ('5', 'Fungicide'),
        ('6', 'Herbicide'),
        ('7', 'Insecticide'),
        ('8', 'Molluscicide'),
        ('9', 'Foliar Fertilizers'),
    )

    dateFrom = forms.DateField(required=True)
    dateTo = forms.DateField(required=True)
    item = forms.ChoiceField(required=True)
    category = forms.ChoiceField(choices=category_list, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].choices = [
            (product.pk, product.item_name) for product in Product.objects.all()
        ]

class ApplyPurchaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Product.objects.none())

    class Meta:
        model = Coupon
        fields = ['farmer', 'saleslady', 'item', 'purchase_date']
        widgets = {'purchase_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Product.objects.order_by('-item_name')
            

class AddPurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0)
    class Meta:
        model = Purchase
        fields = ['purchase_date','item','farmer','saleslady']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type':'date'}),
        }
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].required = True     
  

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

       

    
        


        

        







    
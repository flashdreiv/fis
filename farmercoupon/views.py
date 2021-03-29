from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . forms import GenerateCouponForm,SalesReportForm,ApplyPurchaseForm,ProductForm,AddPurchaseForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from .models import Coupon,Product,Purchase
from accounts.models import Farmer,SalesLady
from django.forms import modelformset_factory
from django.contrib.auth.models import User 
from . generate_random_coupon import generate_coupon_code
import datetime
from django import forms
from django.db.models import F

# Create your views here.

def page404(request):
    return render(request,'farmercoupon/404.html')


@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def manageCoupons(request):
    form = GenerateCouponForm()
    coupon_list = Coupon.objects.order_by('-date_created').exclude(farmer__isnull=False)
    if request.method == 'POST':
        form = GenerateCouponForm(request.POST or None)
        if form.is_valid():
            count = request.POST.get('count')
            count = int(count)
            ticket_value = request.POST.get('ticket_value')
            for x in range(count):
                coupon = Coupon()
                if int(ticket_value) > 14:
                    coupon.is_golden_ticket = True
                coupon.ticket_value = ticket_value   
                coupon.save()
            messages.success(request,f'Generated a total of {count} coupon for a ticket value of {coupon.ticket_value}')
            return redirect('managecoupons')
    context = {
        'form':form,
        'coupons':coupon_list,
    }
    return render(request,'farmercoupon/manage_coupons.html',context)


@login_required
@allowed_users(allowed_roles=['DAS','admin'])
def manageProducts(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'New Product has been created!')
    products = Product.objects.order_by('item_category')
    context = {
        'products':products,
        'form':form
    }
    return render(request,'farmercoupon/manage_products.html',context)

@admin_only
def salesView(request): 
    form = SalesReportForm()
    context = {
        'form':form,
    }   
    return render(request,'farmercoupon/sales_per_item_reports.html',context)
@admin_only
def salesCategory(request): 
    form = SalesReportForm()
    context = {
        'form':form,
    }   
    return render(request,'farmercoupon/sales_per_category_reports.html',context)

@login_required
@allowed_users(allowed_roles=['DAS','admin'])
def viewPurchases(request):
    purchases = Purchase.objects.all()
    context = {
        'purchases':purchases,
    }
    return render(request,'farmercoupon/view_purchases.html',context)

@login_required
@allowed_users(allowed_roles=['DAS','admin'])    
def addPurchase(request):
    AddPurchaseFormset = modelformset_factory(Purchase,
    fields=['purchase_date','farmer','item','saleslady'],
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date','required':True,'autofocus': 'autofocus'}),
            'item': forms.Select(attrs={'required':True}),
            'farmer': forms.Select(attrs={'required':True}),
            'saleslady': forms.Select(attrs={'required':True}),
        }
    )
    formset = AddPurchaseFormset(queryset=Purchase.objects.none())
    if request.method == "POST":
        formset = AddPurchaseFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                farmer = Farmer.objects.get(pk=instance.farmer.id)
                saleslady = SalesLady.objects.get(pk=instance.saleslady.id)
                if instance.item.item_category == '1':
                    farmer.golden_ticket = F('golden_ticket') +1
                    saleslady.golden_ticket = F('golden_ticket') +1
                elif int(instance.item.item_category) > 1:
                    farmer.standard_ticket = F('standard_ticket') +1
                    saleslady.standard_ticket = F('standard_ticket') +1
                saleslady.save()
                farmer.save()
                instance.save()
            messages.success(request,'All Purchase have been saved')
            return redirect('addpurchase')
        else:
            messages.warning(request,'Purchases cant be saved')
            return redirect('addpurchase')
    context = {
        'formset':formset,
    }
    return render(request,'farmercoupon/add_purchase.html',context)


def editProducts(request,pk):
    product = get_object_or_404(Product,pk=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,'Product updated successfully')
            return redirect('manageproducts')
        else:
            messages.warning(request,'Failed to update product details')
    context = {
        'form':form
    }
    return render(request,'farmercoupon/edit_products.html',context)


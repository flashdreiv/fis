from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . forms import GenerateCouponForm,SalesReportForm,ApplyPurchaseForm,ProductForm,AddPurchaseForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from .models import Coupon,Product,Purchases
from accounts.models import Farmer,SalesLady
from django.forms import formset_factory
from django.contrib.auth.models import User 


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

# @login_required
# @allowed_users(allowed_roles=['saleslady'])
# def salesladyView(request):
#     saleslady = request.user.saleslady
#     total_sales = 0
#     try:
#         sales = Coupon.objects.filter(saleslady=saleslady)
#         for sale in sales:
#             total_sales += sales.item.price | 0
#     except:
#         total_sales = 0
#     context = {
#         'sales':total_sales
#     }
#     return render(request,'farmercoupon/saleslady_user.html',context)
    
# @login_required
# @allowed_users(allowed_roles=['DAS','admin'])
# def viewCoupons(request):
#     saleslady = request.user.saleslady
#     total_sales = 0
#     try:
#         sales = Coupon.objects.filter(saleslady=saleslady)
#     except:
#         total_sales = 0
#     context = {
#         'coupons':sales
#     }
#     return render(request,'farmercoupon/saleslady_view_coupons.html',context)

@login_required
@allowed_users(allowed_roles=['DAS','admin'])
def viewPurchases(request,view="generate"):
    form = ApplyPurchaseForm()
    if view == "generate":
        if request.method == "POST":
            count = int(request.POST.get('count'))
            form = ApplyPurchaseForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                for x in range(count):
                    instance.pk = None
                    instance.save()
                messages.success(request,f'Coupon applied successfully')
            else:
                messages.error(request,form.errors)
    else:
        redirect('404')

    # form = ApplyCouponFormBlo()
    # if request.method == "POST":    
    #     form = ApplyCouponFormBlo(request.POST)
    #     if form.is_valid():
    #         saleslady = SalesLady.objects.get(pk=request.POST.get('saleslady'))
    #         farmer = Farmer.objects.get(pk=request.POST.get('farmer'))
    #         item = Product.objects.get(pk=request.POST.get('item'))
    #         ticket_value = item.ticket_value
    #         count = int(request.POST.get('count'))
    #         for x in range(count):
    #             coupon = Coupon.objects.create(code=generate_coupon_code(),saleslady=saleslady,ticket_value=ticket_value,farmer=farmer,item=item,purchase_date=date.today())
    #             if coupon.item.item_category == '1':
    #                 coupon.is_golden_ticket = True
    #                 farmer.golden_ticket+=1
    #             farmer.save()
    #             coupon.save()
    #         form.save()
    #         messages.success(request,f'Coupon applied to {coupon.farmer.user.first_name}')
    #         return redirect('blocoupons')
    #     else:
    #         messages.error(request,'Failed to apply coupon')
    coupons = Coupon.objects.exclude(farmer__isnull=True).order_by('date_created')[:500]
    context = {
        'form': form,
        'coupons':coupons,
        'view':view
    }
    return render(request,'farmercoupon/manage_coupons.html',context)

@login_required
@allowed_users(allowed_roles=['DAS','admin'])    
def addPurchases(request):
    form = AddPurchaseForm()

    AddPurchaseFormset = formset_factory(AddPurchaseForm,extra=2,can_delete=True)

    form = AddPurchaseFormset

    context = {
        'form':form
    }
    return render(request,'farmercoupon/add_purchase.html',context)


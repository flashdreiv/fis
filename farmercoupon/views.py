from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import YFarmerForm,LoginForm,ApplyCouponForm,GenerateCouponForm,SalesReportForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from . models import Farmer,Coupon,Product,Purchase,SalesLady
from django.contrib.auth.models import User,Group
from . generate_random_coupon import generate_coupon_code
from django.http import JsonResponse

#django rest framework
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response


# Create your views here.


@login_required(login_url='login')
@admin_only
def adminView(request):
    return render(request,'farmercoupon/admin.html')

@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = YFarmerForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='farmer')
            user.groups.add(group)
            farmer = Farmer()
            farmer.user = user
            farmer.save()
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = YFarmerForm()
    return render(request,'farmercoupon/register.html',{'form':form})

@unauthenticated_user
def loginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            messages.error(request, 'Incorrect Login credentials')
    return render(request, 'farmercoupon/login.html', {'form': form})

@login_required(login_url='login')
def logOutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['farmer'])
def userPage(request):
    form = ApplyCouponForm()
    if request.method == 'POST':
        form = ApplyCouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            saleslady = SalesLady.objects.get(pk=int(form.cleaned_data['saleslady']))
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                    is_used=False,
                    is_active=True
                )
                request.session['coupon_id'] = coupon.id
                coupon.farmer = request.user.farmer
                farmer = request.user.farmer
                #Check if golden ticket
                if(coupon.is_golden_ticket):
                    farmer.golden_ticket+=1
                    saleslady.golden_ticket+=1
                else:
                    farmer.standard_ticket+=coupon.item.ticket_value
                    saleslady.standard_ticket+=coupon.item.ticket_value
                #if coupon is applied add a purchase for the farmer
                purchase = Purchase(farmer=farmer,coupon=coupon,item=coupon.item,saleslady=saleslady)
                purchase.save()
                coupon.is_used = True
                farmer.save()
                saleslady.save()
                coupon.saleslady = saleslady
                coupon.save()
                messages.success(request,'Successfully submitted ticket')
                return redirect('user')
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                messages.error(request,'Coupon does not exist')         
    return render(request,'farmercoupon/standard_user.html',{'form':form})
    
@admin_only
@login_required(login_url='login')
def manageUsers(request):
    users = User.objects.all().exclude(groups = 1)
    context = {
        'users':users
    }
    return render(request,'farmercoupon/manageUsers.html',context)

@admin_only
@login_required(login_url='login')
def manageCoupons(request):
    form = GenerateCouponForm(request.POST or None)
    coupon_list = Coupon.objects.order_by('-date_created')
    if request.method == 'POST':
        if form.is_valid():
            count = request.POST.get('count')
            count = int(count)
            item_id = request.POST.get('item')
            for x in range(count):
                coupon = Coupon()
                coupon.item = Product.objects.get(pk=item_id)
                if coupon.item.pk == 3 or coupon.item.pk == 4 or coupon.item.pk == 5:
                    coupon.is_golden_ticket = True
                code = generate_coupon_code()
                coupon.code = code
                coupon.save()
            messages.success(request,f'Generated a total of {count} coupon for {coupon.item.item_name}')
        else:
            form = GenerateCouponForm()
    context = {
        'form':form,
        'coupons':coupon_list
    }
    return render(request,'farmercoupon/manage_coupons.html',context)
    
@admin_only
def manageProducts(request):
    products = Product.objects.order_by('item_category')
    context = {
        'products':products
    }
    return render(request,'farmercoupon/manage_products.html',context)

@admin_only
def salesView(request): 
    form = SalesReportForm()
    context = {
        'form':form,
    }   
    return render(request,'farmercoupon/sales_reports.html',context)
         
# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def SalesReportApi(request):
#     purchase = Purchase.objects.count()
#     item = request.GET.get('item')
#     labels = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
#     defaultData = [1,2,3,4,5,6,7,8,9,10,11,12]
#     data = {
#             'purchase': purchase,
#             'labels':labels,
#             'defaultData':defaultData,
#             'item':item
#         }
#     return Response(data)
    

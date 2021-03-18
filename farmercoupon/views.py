from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import YFarmerForm,LoginForm,ApplyCouponForm,GenerateCouponForm,SalesReportForm,ApplyCouponFormBlo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from . models import Farmer,Coupon,Product,SalesLady
from django.contrib.auth.models import User,Group
from . generate_random_coupon import generate_coupon_code
from datetime import date

from django.db.models import Sum
# Create your views here.


@login_required(login_url='login')
@admin_only
def adminView(request):
    total_sales = 0
    total_golden_ticket = 0
    total_ticket = 0
    context = {}
    try:
        purchases = Coupon.objects.exclude(farmer__isnull=True)
        total_golden_ticket = Coupon.objects.filter(farmer__isnull=False,is_golden_ticket=True).count()
        total_ticket = Coupon.objects.filter(farmer__isnull=False,is_golden_ticket=False).count()
        for purchase in purchases:
            total_sales += purchase.item.price
    except:
        pass
    context = {
        'total_sales':int(total_sales),
        'total_ticket':total_ticket,
        'total_golden_ticket':total_golden_ticket
    }
    print(total_ticket)
    return render(request,'farmercoupon/admin.html',context)

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
                # purchase = Purchase(farmer=farmer,coupon=coupon,item=coupon.item,saleslady=saleslady)
                # purchase.save()
                # coupon.is_used = True
                coupon.purchase_date = date.today()
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
            # item_id = request.POST.get('item')
            ticket_value = request.POST.get('ticket_value')
            for x in range(count):
                coupon = Coupon()
                # coupon.item = Product.objects.get(pk=item_id)
                # if coupon.item.pk == 3 or coupon.item.pk == 4 or coupon.item.pk == 5:
                #     coupon.is_golden_ticket = True
                if int(ticket_value) > 14:
                    coupon.is_golden_ticket = True
                coupon.ticket_value = ticket_value   
                coupon.code = generate_coupon_code()
                coupon.save()
            messages.success(request,f'Generated a total of {count} coupon for a ticket value of {coupon.ticket_value}')
            return redirect('managecoupons')
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

@login_required
@allowed_users(allowed_roles=['saleslady'])
def salesladyView(request):
    saleslady = request.user.saleslady
    total_sales = 0
    try:
        sales = Coupon.objects.filter(saleslady=saleslady)
        for sale in sales:
            total_sales += sales.item.price | 0
    except:
        total_sales = 0
    context = {
        'sales':total_sales
    }
    return render(request,'farmercoupon/saleslady_user.html',context)
    
@login_required
@allowed_users(allowed_roles=['saleslady'])
def viewCoupons(request):
    saleslady = request.user.saleslady
    total_sales = 0
    try:
        sales = Coupon.objects.filter(saleslady=saleslady)
    except:
        total_sales = 0
    context = {
        'coupons':sales
    }
    return render(request,'farmercoupon/saleslady_view_coupons.html',context)

@login_required
@admin_only
def manageBlo(request):
    form = ApplyCouponFormBlo()
    if request.method == "POST":
        if form_is_valid():
            saleslady = request.POST.get('saleslady')
            farmer = request.POST.get('farmer')
            item = request.POST.get('item')
            ticket_value = request.POST.get('ticket_value')
            count = request.POST.get('count')
            for x in count:
                coupon = Coupon.objects.bulk_create(code=generate_coupon_code(),saleslady=saleslady,farmer=farmer,item=item,ticket_value=ticket_value)
            coupon.save()
            message.success(f'Coupon applied to {coupon.farmer.user.first_name}')
        else:
            messages.error(request,'Failed to apply coupon')
    context = {
        'form': form,
    }
    return render(request,'farmercoupon/manage_coupons.html',context)
         
def viewSms(request):
    return render(request,'farmercoupon/sms.html')
    

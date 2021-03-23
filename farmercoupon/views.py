from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . forms import LoginForm,ApplyCouponForm,GenerateCouponForm,SalesReportForm,ApplyCouponFormBlo,AddFarmerForm,ProductForm,SalesLadyForm,UserForm,ChangePasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from . models import Farmer,Coupon,Product,SalesLady
from django.contrib.auth.models import User,Group
from . generate_random_coupon import generate_coupon_code
from datetime import date

from django.db.models import Sum
# Create your views here.

def index(request):
    return render(request,'farmercoupon/homepage.html')

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

# @unauthenticated_user
# def register(request):
#     if request.method == "POST":
#         form = YFarmerForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             group = Group.objects.get(name='farmer')
#             user.groups.add(group)
#             farmer = Farmer()
#             farmer.user = user
#             farmer.save()
#             messages.success(request,f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = YFarmerForm()
#     return render(request,'farmercoupon/register.html',{'form':form})

@unauthenticated_user
def loginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin')
            else:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Incorrect Login credentials')
    return render(request, 'farmercoupon/login.html', {'form': form})


@login_required(login_url='login')
def logOutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Farmer','Saleslady'])
def userProfile(request):
    if request.user.saleslady or request.user.farmer:
        if request.user.saleslady.is_new_user:
            return redirect('changepassword')
        #Later for farmer coupon application
        form = ApplyCouponForm()
        
        saleslady = request.user.saleslady
        total_sales = 0
        try:
            sales = Coupon.objects.filter(saleslady=saleslady)
            for sale in sales:
                total_sales += sale.item.price | 0
        except:
            total_sales = 0

        context = {
            'form':form,
            'total_sales':total_sales
        }

        
    # form = ApplyCouponForm()
    # if request.method == 'POST':
    #     form = ApplyCouponForm(request.POST)
    #     if form.is_valid():
    #         code = form.cleaned_data['code']
    #         saleslady = SalesLady.objects.get(pk=int(form.cleaned_data['saleslady']))
    #         try:
    #             coupon = Coupon.objects.get(code__iexact=code,
    #                 is_used=False,
    #                 is_active=True
    #             )
    #             request.session['coupon_id'] = coupon.id
    #             coupon.farmer = request.user.farmer
    #             farmer = request.user.farmer
    #             if(coupon.is_golden_ticket):
    #                 farmer.golden_ticket+=1
    #                 saleslady.golden_ticket+=1
    #             else:
    #                 farmer.standard_ticket+=coupon.item.ticket_value
    #                 saleslady.standard_ticket+=coupon.item.ticket_value
    #             coupon.purchase_date = date.today()
    #             farmer.save()
    #             saleslady.save()
    #             coupon.saleslady = saleslady
    #             coupon.save()
    #             messages.success(request,'Successfully submitted ticket')
    #             return redirect('user')
    #         except Coupon.DoesNotExist:
    #             request.session['coupon_id'] = None
    #             messages.error(request,'Coupon does not exist')         
    return render(request,'farmercoupon/standard_user.html',context)
    
@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def manageUsers(request):
    users = User.objects.filter(groups__name__in=['Farmer','Saleslady'])
    context = {
        'users':users
    }
    return render(request,'farmercoupon/manageUsers.html',context)

@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def addUsers(request,fuser="Farmer"):
    userForm = UserForm()
    form = AddFarmerForm() if fuser == 'Farmer' else SalesLadyForm()
    if request.method == "POST":
        form = AddFarmerForm(request.POST or None) if fuser == 'Farmer' else SalesLadyForm(request.POST or None)
        userForm = UserForm(request.POST)
        if form.is_valid() and userForm.is_valid():
            user = userForm.save()
            user_details = form.save(commit=False)
            group = Group.objects.get(name=fuser)
            user_details.user = user
            user_details.user.groups.add(group)
            user_details.save()
            messages.success(request,"User added Successfully!")
            return redirect('manageusers')
        else:
            messages.warning(request,form.errors)
            messages.warning(request,userForm.errors)
            return redirect("manageusers")
    context = {
        'form':form,
        'userForm':userForm,
        'usertype':fuser
    }
    return render(request,'farmercoupon/add_user.html',context)

@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def editUsers(request,fuser,pk):
    #UserForm
    user = get_object_or_404(User,pk=pk)
    editUserForm = UserForm(instance=user)
    #FarmerForm or SalesladyForm
    member = Farmer.objects.get(user=user) if fuser == "Farmer" else SalesLady.objects.get(user=user)
    editForm = AddFarmerForm(instance=member) if fuser == "Farmer" else SalesLadyForm(instance=member)
    if request.method == "POST":
        editForm = AddFarmerForm(request.POST, instance=member)
        editUserForm = UserForm(request.POST,instance=user)
        if editForm.is_valid() and editUserForm.is_valid():
            editForm.save()
            editUserForm.save()
            messages.success(request,'Farmer information updated successfully')
            return redirect('manageusers')
        else:
            messages.warning(request,editForm.errors)
    context = {
        'form':editForm,
        'userForm':editUserForm
    }
    return render(request,'farmercoupon/edit_users.html',context)
    

@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def manageCoupons(request):
    form = GenerateCouponForm(request.POST or None)
    coupon_list = Coupon.objects.order_by('-date_created').exclude(farmer__isnull=False)
    if request.method == 'POST':
        if form.is_valid():
            count = request.POST.get('count')
            count = int(count)
            ticket_value = request.POST.get('ticket_value')
            for x in range(count):
                coupon = Coupon()
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
def manageBlo(request):
    form = ApplyCouponFormBlo()
    if request.method == "POST":    
        form = ApplyCouponFormBlo(request.POST)
        if form.is_valid():
            saleslady = SalesLady.objects.get(pk=request.POST.get('saleslady'))
            farmer = Farmer.objects.get(pk=request.POST.get('farmer'))
            item = Product.objects.get(pk=request.POST.get('item'))
            ticket_value = item.ticket_value
            count = int(request.POST.get('count'))
            for x in range(count):
                coupon = Coupon.objects.create(code=generate_coupon_code(),saleslady=saleslady,ticket_value=ticket_value,farmer=farmer,item=item,purchase_date=date.today())
                if coupon.item.item_category == '1':
                    coupon.is_golden_ticket = True
                    farmer.golden_ticket+=1
                farmer.save()
                coupon.save()
            messages.success(request,f'Coupon applied to {coupon.farmer.user.first_name}')
            return redirect('blocoupons')
        else:
            messages.error(request,'Failed to apply coupon')
    coupons = Coupon.objects.exclude(farmer__isnull=True)
    context = {
        'form': form,
        'coupons':coupons
    }
    return render(request,'farmercoupon/manage_coupons.html',context)
         
@login_required
@allowed_users(allowed_roles=['admin','DAS','Farmer','Saleslady'])
def changePassword(request):
    if request.user.saleslady:
        if not request.user.saleslady.is_new_user:
            return redirect('profile')
               
    form = ChangePasswordForm(request.user)
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if(user.saleslady.is_new_user):
                user.saleslady.is_new_user = False
                user.saleslady.save()
                user.save()
            messages.success(request,'Password successfully changed!')
            return redirect('logout')
        else:
            messages.warning(request,'Error changing password!')
    context = {
        'form':form
    }
    return render(request,'farmercoupon/changepasswd.html',context)
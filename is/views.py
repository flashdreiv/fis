from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import YFarmerForm,LoginForm,ApplyCouponForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from . models import Farmer,Coupon
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.

@login_required(login_url='login')
@admin_only
def adminView(request):
    return render(request,'is/admin.html')

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
    return render(request,'is/register.html',{'form':form})

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
    return render(request, 'is/login.html', {'form': form})

@login_required(login_url='login')
def logOutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['farmer'])
def userPage(request):
    form = ApplyCouponForm()
    now = timezone.now()
    if request.method == 'POST':
        form = ApplyCouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                    is_used=False,
                    is_active=True
                )
                request.session['coupon_id'] = coupon.id
                coupon.farmer = request.user.farmer
                farmer = request.user.farmer
                saleslady = coupon.saleslady
                #Check if golden ticket
                if(coupon.is_golden_ticket):
                    farmer.golden_ticket+=1
                    saleslady.golden_ticket+=1
                else:
                    farmer.standard_ticket+=coupon.item.ticket_value
                    saleslady.standard_ticket+=coupon.item.ticket_value
                coupon.is_used = True
                farmer.save()
                saleslady.save()
                coupon.save()
                messages.success(request,'Successfully submitted ticket')
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                messages.error(request,'Coupon does not exist')
    return render(request,'is/farmer.html',{'form':form})
    
@admin_only
def manageUsers(request):
    users = User.groups.get(name__iexact='farmer')
    context = {
        'users':users
    }
    return render(request,'is/manageUsers.html',context)
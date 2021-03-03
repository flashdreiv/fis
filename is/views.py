from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import YFarmerForm,LoginForm,ApplyCouponForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from . models import Farmer,Coupon
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
    now = timezone.now()
    form = ApplyCouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                is_active=True
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
        
    return render(request,'is/farmer.html',{'form':form})
    

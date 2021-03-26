from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from accounts.forms import LoginForm,AddFarmerForm,SalesLadyForm,UserForm,ChangePasswordForm,UpdateUserForm,ApplyCouponForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from farmercoupon.decorators import unauthenticated_user,allowed_users,admin_only
from farmercoupon.models import Farmer,Coupon,Product,SalesLady
from django.contrib.auth.models import User,Group

# Create your views here.


@unauthenticated_user
def loginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        group = Group.objects.filter(user=user)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin')
            elif group[0].name == 'DAS':
                return redirect('manageusers')
            else:
                return redirect('profile')
        else:
            messages.error(request, 'Incorrect Login credentials')
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def logOutUser(request):
    logout(request)
    return redirect('login')


@login_required
@allowed_users(allowed_roles=['Farmer','Saleslady'])
def changePassword(request):

    user_group = Group.objects.get(user=request.user)
    user_group = user_group.name
    user1 = request.user.farmer if user_group == "Farmer" else request.user.saleslady

    form = ChangePasswordForm(user1)

    if user_group == "Saleslady":
        if not user1.is_new_user:
            return redirect('profile')
        else:
            if request.method == "POST":
                form = ChangePasswordForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.saleslady.is_new_user = False
                    user.saleslady.save()
                    user.save()
                    messages.success(request,'Password successfully changed!')
                    return redirect('logout')
                else:
                    messages.warning(request,'Error changing password!')
    elif user_group == "Farmer":
        if not user1.is_new_user:
            return redirect('profile')     
        else:
           if request.method == "POST":
                form = ChangePasswordForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.farmer.is_new_user = False
                    user.farmer.save()
                    user.save()
                    messages.success(request,'Password successfully changed!')
                    return redirect('logout')
                else:
                    messages.warning(request,'Error changing password!') 
    context = {
        'form':form
    }
    return render(request,'accounts/changepasswd.html',context)



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
    return render(request,'accounts/admin.html',context)

@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def manageUsers(request):
    users = User.objects.filter(groups__name__in=['Farmer','Saleslady'])
    context = {
        'users':users
    }
    return render(request,'accounts/manageUsers.html',context)
  

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
    return render(request,'accounts/add_user.html',context)

@allowed_users(allowed_roles=['DAS','admin'])
@login_required(login_url='login')
def editUsers(request,fuser,pk):
    #UserForm
    user = get_object_or_404(User,pk=pk)
    editUserForm = UpdateUserForm(instance=user)
    #FarmerForm or SalesladyForm
    member = Farmer.objects.get(user=user) if fuser == "Farmer" else SalesLady.objects.get(user=user)
    editForm = AddFarmerForm(instance=member) if fuser == "Farmer" else SalesLadyForm(instance=member)
    if request.method == "POST":
        editForm = AddFarmerForm(request.POST, instance=member) if fuser == "Farmer" else SalesLadyForm(request.POST,instance=member)
        editUserForm = UpdateUserForm(request.POST,instance=user)
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
    return render(request,'accounts/edit_users.html',context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['Farmer','Saleslady'])
def userProfile(request):
    user_group = Group.objects.get(user=request.user)
    user_group = user_group.name
    user = request.user.farmer if user_group == "Farmer" else request.user.saleslady
    form = ApplyCouponForm()
    total_sales = 0
    if user_group == "Saleslady":
        if user.is_new_user:
            return redirect('changepassword')
        else:
            try:
                sales = Coupon.objects.filter(saleslady=user)
                for sale in sales:
                    total_sales += sale.item.price | 0
            except:
                total_sales = 0
    elif user_group == "Farmer":
            if user.is_new_user:
                return redirect('changepassword')
            else:
                try:
                    sales = Coupon.objects.filter(farmer=user)
                    for sale in sales:
                        total_sales += sale.item.price | 0
                except:
                    total_sales = 0
    context = {
        'form':form,
        'total_sales':total_sales
    }     
    return render(request,'accounts/standard_user.html',context)
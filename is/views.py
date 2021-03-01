from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import YFarmerForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user
# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request,'is/index.html')

@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = YFarmerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
            return redirect('index')
        else:
            messages.error(request, 'Incorrect Login credentials')
    return render(request, 'is/login.html', {'form': form})

@login_required(login_url='login')
def logOutUser(request):
    logout(request)
    return render(request,'is/logout.html')


def userPage(request):
    return render(request,'is/farmer.html')
    

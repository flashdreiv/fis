from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied

def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        group = None
        if request.user.is_authenticated:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'admin': 
                return redirect('admin')
            if group == 'Saleslady': 
                return redirect('profile')
            if group == "DAS":
                return redirect('manageusers')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin': 
           return view_func(request, *args,**kwargs)
        if group == 'Saleslady' or group == 'Farmer': 
            return redirect('profile')
        if group == 'DAS': 
           return redirect('manageusers')
        else:
            return redirect('profile')
    return wrapper_func



from django.urls import path
from . import views


urlpatterns = [
    path('',views.loginPage,name='index'),
    path('django-admin',views.adminView,name='admin'),
    path('register',views.register,name='register'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logOutUser,name='logout'),
    path('user',views.userPage,name='user'),
    path('manageusers',views.manageUsers,name='managusers'),

]
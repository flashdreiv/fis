from django.urls import path
from . import views

#User django-all auth


urlpatterns = [
    path('',views.loginPage,name='index'),
    path('django-admin',views.adminView,name='admin'),
    path('register',views.register,name='register'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logOutUser,name='logout'),
    path('user',views.userPage,name='user'),
    path('manageusers',views.manageUsers,name='manageusers'),
    path('manageusers/edit/<int:pk>',views.editUsers,name='editusers'),
    path('managecoupons',views.manageCoupons,name='managecoupons'),
    path('manageproducts',views.manageProducts,name='manageproducts'),
    path('sales/item/',views.salesView,name='salesperitem'),
    path('sales/category/',views.salesCategory,name='salespercategory'),
    #Sales lady views
    path('saleslady',views.salesladyView,name='saleslady'),
    # path('viewcoupons',views.viewCoupons,name='viewcoupons'),
    #Big land owner views
    path('blocoupons',views.manageBlo,name='blocoupons'),
    
   
]
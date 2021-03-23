from django.urls import path
from . import views

#User django-all auth


urlpatterns = [
    path('',views.index,name='index'),
    path('accounts/profile',views.userProfile,name='profile'),
    path('accounts/admin',views.adminView,name='admin'),
    path('accounts/login',views.loginPage,name='login'),
    path('accounts/logout',views.logOutUser,name='logout'),
    path('accounts/changepasswd',views.changePassword,name='changepassword'),
    path('accounts/manageusers',views.manageUsers,name='manageusers'),
    path('accounts/manageusers/add/<fuser>/',views.addUsers,name='addusers'),
    path('accounts/manageusers/edit/<fuser>/<int:pk>',views.editUsers,name='editusers'),
    path('managecoupons',views.manageCoupons,name='managecoupons'),
    path('manageproducts',views.manageProducts,name='manageproducts'),
    path('sales/item/',views.salesView,name='salesperitem'),
    path('sales/category/',views.salesCategory,name='salespercategory'),
    #Sales lady views
    # path('saleslady',views.salesladyView,name='saleslady'),
    # path('viewcoupons',views.viewCoupons,name='viewcoupons'),
    #Big land owner views
    path('blocoupons',views.manageBlo,name='blocoupons'),
    
   
]
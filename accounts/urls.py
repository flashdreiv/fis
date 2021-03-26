from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage,name='index'),
    path('accounts',views.loginPage,name='index'),
    path('profile',views.userProfile,name='profile'),
    path('admin',views.adminView,name='admin'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logOutUser,name='logout'),
    path('changepasswd',views.changePassword,name='changepassword'),
    path('manageusers',views.manageUsers,name='manageusers'),
    path('manageusers/add/<fuser>/',views.addUsers,name='addusers'),
    path('manageusers/edit/<fuser>/<int:pk>',views.editUsers,name='editusers')   
]
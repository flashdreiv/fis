from django.urls import path
from . import views

#User django-all auth


urlpatterns = [
    
    path('404',views.page404,name='404'),
    path('managecoupons/manage',views.manageCoupons,name='managecoupons'),
    path('manageproducts',views.manageProducts,name='manageproducts'),
    path('sales/item/',views.salesView,name='salesperitem'),
    path('sales/category/',views.salesCategory,name='salespercategory'),
    #Sales lady views
    # path('saleslady',views.salesladyView,name='saleslady'),
    # path('viewcoupons',views.viewCoupons,name='viewcoupons'),
    #Big land owner views
    path('purchases/view',views.viewPurchases,name='viewpurchases'),
    path('purchases/add',views.addPurchases,name='addpurchases'),
    
   
]
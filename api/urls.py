from django.urls import path
from . import views

urlpatterns = [  
    path('sales/',views.SalesReportApi,name='getsales'),
    path('revenue/',views.revenue,name='getrevenue'),
    path('sms/',views.viewSms,name='sms'),
]
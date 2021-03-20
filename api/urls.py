from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [  
    path('sales/',views.SalesReportApi,name='getsales'),
    path('revenue/',views.revenue,name='getrevenue'),
    path('sms/receive',csrf_exempt(views.receiveSms),name='sms-receive'),
    path('sms/register',csrf_exempt(views.registerNumber),name='sms-register'),
    path('location/provinces',views.loadProvinces,name='load-provinces'),
    path('location/cities',views.loadCities,name='load-cities'),
    path('location/barangays',views.loadBarangays,name='load-barangays'),
]

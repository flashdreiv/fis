from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from is.models import Purchase


@api_view(["GET"])
@permission_classes([IsAdminUser])
def SalesReportApi(request):
    purchase = Purchase.objects.count()
    item = request.GET.get('item')
    labels = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
    defaultData = [1,2,3,4,5,6,7,8,9,10,11,12]
    data = {
            'purchase': purchase,
            'labels':labels,
            'defaultData':defaultData,
            'item':item
        }
    return Response(data)
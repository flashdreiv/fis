from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAdminUser])
def SalesReportApi(request):
    item = request.GET.get('item')
    labels = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
    defaultData = [1,2,3,4,5,6,7,8,9,10,11,12]
    data = {
            'labels':labels,
            'defaultData':defaultData,
            'item':item
        }
    return Response(data)
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from farmercoupon.models import Coupon
from django.db.models import Sum
from . sales_report_manipulation import get_purchase_list,get_purchase_list_item

@api_view(["POST"])
@permission_classes([IsAdminUser])
def SalesReportApi(request):    
    if request.method == "POST":
        dateFrom = request.POST.get('dateFrom')
        dateTo = request.POST.get('dateTo')
        item = request.POST.get('item')
        purchases = Coupon.objects.filter(item=item,purchase_date__gte=dateFrom,purchase_date__lte=dateTo).order_by('purchase_date__month')
        result = get_purchase_list(purchases)
        months = dict.keys(result)
        defaultData = [] 
        for key in result:
            defaultData.append(result[key])
        data = {
            'labels':months,
            'defaultData':defaultData,
            'item':item
            }
    return Response(data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def revenue(request):
    revenue_list = []
    try:
        purchases = Coupon.objects.filter(item__lte=5)
        data = get_purchase_list_item(purchases)
        for key in data:
            revenue_list.append(data[key])
    except:
        revenue_list = []
    data = {
        'revenue':revenue_list
    }
    return Response(data)

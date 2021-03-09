from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from farmercoupon.models import Purchase
from django.db.models import Sum

@api_view(["POST"])
@permission_classes([IsAdminUser])
def SalesReportApi(request):    
    if request.method == "POST":
        total_sales = 0
        dateFrom = request.POST.get('dateFrom')
        dateTo = request.POST.get('dateTo')
        item = request.POST.get('item')
        total_sales_object = Purchase.objects.filter(item=item,purchase_date__gte=dateFrom,purchase_date__lte=dateTo)
        for purchase in total_sales_object:
            total_sales += purchase.item.price
        labels = ["January"]
        defaultData = [total_sales]
        print(total_sales)
        data = {
            'labels':labels,
            'defaultData':defaultData,
            'item':item
            }
    return Response(data)
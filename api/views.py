from django.shortcuts import render
import json
# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from farmercoupon.models import Coupon
from django.db.models import Sum
from . sales_report_manipulation import get_purchase_list,get_purchase_list_item
from . globe import Globe

#Globe API
APP_ID = "6GoBCE4MMeCp5ir5zdcMnGC8kGjnC4jj"
APP_SECRET = "5dd3199550d21e5ce5120c7ebf612b9518b84869945b5333d51a6aae59783c17"
CODE = "yHRpLEaFoGpyjUzBR5AsxKxEKFRyakzSjg4njtdX4GyC7rqrdHkLz8xhj9r4kUaBEg5Ian4n7hzRLrkIBMdpMIbegaBCqGagLszAebBC8kG54Uajno7FxdBEoC7kiRoyB7XTB8GCdXnqdF49G4aUXMe96CBda8EsABggrC7bdkdIBxLjdIep4qAh9xEgaI8jrkEUxyz5AhgEq9GH8j4KXCX64aqt47a7ESp9xk7FroR4BsLAp9AUMeL5kFMLdzEH"
SHORT_CODE ="7517"

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

@api_view(["POST"])
def receiveSms(request):
    inbound_sms = {}
    if request.method == "POST":    
        inbound_sms = request.body.decode('utf-8')
        json_body = json.loads(inbound_sms)
        print(json_body['inboundSMSMessageList'])
    return Response(inbound_sms)

@api_view(["GET"])
def registerNumber(request):
    CODE = request.GET.get('code')
    globe = Globe(APP_ID,APP_SECRET,CODE,SHORT_CODE)
    data = globe.getAccessToken()
    return Response(data)
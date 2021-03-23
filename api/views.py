from django.shortcuts import render
import json
# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from farmercoupon.models import Coupon,Farmer
from django.db.models import Sum
from . sales_report_manipulation import get_purchase_list,get_purchase_list_item
from . globe import Globe
from ph_locations . models import Region,Province,City,Barangay


#Globe API
APP_ID = "6GoBCE4MMeCp5ir5zdcMnGC8kGjnC4jj"
APP_SECRET = "5dd3199550d21e5ce5120c7ebf612b9518b84869945b5333d51a6aae59783c17"
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
    sms_response = ''
    if request.method == "POST":    
        inbound_sms = request.body.decode('utf-8')
        json_body = json.loads(inbound_sms)
        sender_number = json_body['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress'][4:]
        sender_message = json_body['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
        print(json_body)
        print(sender_number)
        try:
            farmer = Farmer.objects.get(mobile_number__iexact=sender_number)
            print('meron dito')
            if(farmer.first_name and farmer.last_name and farmer.globe_code):
                #intialize globe api
                globe = Globe(app_id=APP_ID,app_secret=APP_SECRET,code=farmer.globe_code,short_code=short_code)
                print('meron dit3')
                data = globe.getAccessToken()
                try:
                    coupon = Coupon.objects.get(code__iexact=sender_message,farmer__isnull=True)
                    coupon.farmer = farmer
                    if(coupon.is_golden_ticket):
                        farmer.golden_ticket +=1
                    else:
                        farmer.standard_ticket += coupon.ticket_value       
                    farmer.save()
                    coupon.save()
                    sms_response = globe.sendSms(data['access_token'],sender_number,f'Congratulations {farmer.first_name} you have now a total of Golden ticket: {farmer.golden_ticket} Standard Ticket: {farmer.standard_ticket}')
                except Coupon.DoesNotExist:
                    sms_response = globe.sendSms(data['access_token'],sender_number,f'Invalid coupon entered')
            else:
                sms_response = 'Please complete first your user registration!'
        except:
            sms_response = 'Farmer does not exist'
        print(sms_response)
    return Response(sms_response)


@api_view(["GET"])
def registerNumber(request):
    CODE = request.GET.get('code')
    globe = Globe(APP_ID,APP_SECRET,CODE,SHORT_CODE)
    data = globe.getAccessToken()
    return Response(data)

@api_view(["POST"])
def loadProvinces(request):
    if request.method == "POST":    
        region_id = request.POST.get('id_region')
        province = Province.objects.filter(region_id=region_id)
    return Response(list(province.values('id','name')))

@api_view(["POST"])
def loadCities(request):
    if request.method == "POST":    
        province_id = request.POST.get('id_province')
        city = City.objects.filter(province_id=province_id)
    return Response(list(city.values('id','name')))

@api_view(["POST"])
def loadBarangays(request):
    if request.method == "POST":    
        city_id = request.POST.get('id_city')
        barangays = Barangay.objects.filter(city_id=city_id)
    return Response(list(barangays.values('id','name')))

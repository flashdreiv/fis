import requests,json

access_token = "2RZVZRABtcYrCSFQw_ouRXu1xXNi318bGbwRLbnyKGM"
APP_ID = "6GoBCE4MMeCp5ir5zdcMnGC8kGjnC4jj"
APP_SECRET = "5dd3199550d21e5ce5120c7ebf612b9518b84869945b5333d51a6aae59783c17"
CODE = "yHRpLEaFoGpyjUzBR5AsxKxEKFRyakzSjg4njtdX4GyC7rqrdHkLz8xhj9r4kUaBEg5Ian4n7hzRLrkIBMdpMIbegaBCqGagLszAebBC8kG54Uajno7FxdBEoC7kiRoyB7XTB8GCdXnqdF49G4aUXMe96CBda8EsABggrC7bdkdIBxLjdIep4qAh9xEgaI8jrkEUxyz5AhgEq9GH8j4KXCX64aqt47a7ESp9xk7FroR4BsLAp9AUMeL5kFMLdzEH"
SHORT_CODE ="7517"

class Globe:
    def __init__(self,app_id,app_secret,code,short_code):
        self.app_id = app_id
        self.app_secret = app_secret
        self.code = code
        self.short_code = short_code

    #Get access token
    def getAccessToken(self):
        url_access_token = f'https://developer.globelabs.com.ph/oauth/access_token?app_id={self.app_id}&app_secret={self.app_secret}&code={self.code}'
        r = requests.post(url_access_token)
        return r.json()
    
    #Send sms
    def sendSms(self,access_token,address,message):
        url_send_sms = f'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/{self.short_code}/requests?access_token={access_token}'
        body = {"outboundSMSMessageRequest": {
                    "clientCorrelator": "123456",
                    "senderAddress": self.short_code,
                    "outboundSMSTextMessage": {"message": message},
                    "address": address
                    }
                }  
        json_body = json.dumps(body)
        headers = {'content-type': 'application/json'}
        r = requests.post(url_send_sms,data=json_body,headers=headers)
        return r.json()
        
        
# globe = Globe(APP_ID,APP_SECRET,CODE,SHORT_CODE)
# data = globe.getAccessToken()
#print(globe.sendSms(data['access_token'],data['subscriber_number'],'Hello fuckers'))













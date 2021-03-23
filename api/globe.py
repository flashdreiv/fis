import requests,json

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













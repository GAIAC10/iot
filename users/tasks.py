from django.conf import settings
from tools.sms import YunTongXin

def send_sms_c(phone,code):
    config={
        # 'accountSid':settings.ACCOUNTSID,
        # 'accountToken':settings.ACCOUNTTOKEN,
        # 'appId':settings.APPID,
        # 'templateId':settings.TEMPLATEID

    'accountSid':'8aaf07087a331dc7017ad92a25cb33cb',
    'accountToken':'895fc86f9cec4525b9fedaf849e12d41',
    'appId':'8aaf07087a331dc7017ad92a26c433d1',
    'templateId':'1'
    }
    yun=YunTongXin(**config)
    res=yun.run(phone,code)
    return res
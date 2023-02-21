import datetime
import hashlib
import base64
# 发送http/hrrps请求
import requests
import json

class YunTongXin():
    # 无论是哪个账户，base_url都不变
    base_url='https://app.cloopen.com:8883'

    def __init__(self,accountSid,accountToken,appId,templateId):
        # 账户ID
        self.accountSid=accountSid
        # 授权令牌
        self.accountToken=accountToken
        # 应用ID
        self.appId=appId
        # 模板ID
        self.templateId=templateId

    def get_request_url(self,sig):
    # 业务URL格式：/2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
    # {SigParameter}是：
    # 1.使用MD5加密（账户Id + 账户授权令牌 + 时间戳）。其中账户Id和账户授权令牌根据url的验证级别对应主账户。时间戳是当前系统时间，格式"yyyyMMddHHmmss"。时间戳有效时间为24小时，如：20140416142030
    # 2.SigParameter参数需要大写，如不能写成sig=abcdefg而应该写成sig=ABCDEFG
        self.url=self.base_url+'/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid,sig)
        return self.url

    # 生成时间戳
    def get_timestamp(self):
        # .strftime()是时间的格式化:一大带两小，三大
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # 生成sig={SigParameter}
    def get_sig(self,timestamp):
        s=self.accountSid+self.accountToken+timestamp
        m=hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    # HTTP标准包头字段验证信息:
    # （1）Authorization 1.使用Base64编码（账户Id + 冒号 + 时间戳）其中账户Id根据url的验证级别对应主账户。2.冒号为英文冒号。3.时间戳是当前系统时间，格式"yyyyMMddHHmmss"，需与SigParameter中时间戳相同。
    # （2）Accept application/json
    # （3）Content-Type application/json;charset=utf-8
    def get_request_header(self,timestamp):
        # 生成请求头
        s=self.accountSid+':'+timestamp
        auth=base64.b64encode(s.encode()).decode()
        return {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization':auth,
        }

    def get_request_body(self,phone,code):
        return {
            'to':phone,
            'appId':self.appId,
            'templateId':self.templateId,
            # code是验证码，3是3分钟
            'datas':[code,'3']
        }

    # 给云通信发送请求
    def request_api(self,url,header,body):
        # res是云通信返回的 对象
        res=requests.post(url,headers=header,data=body)
        return res.text

    def run(self,phone,code):
        # 获取时间戳
        timestamp=self.get_timestamp()
        # 生成签名
        sig=self.get_sig(timestamp)
        # 生成业务url
        url=self.get_request_url(sig)
        # 生成请求头
        header=self.get_request_header(timestamp)
        # 生成请求体
        body=self.get_request_body(phone,code)
        # 发送请求
        data=self.request_api(url,header,json.dumps(body))
        return data

# 测试版（写死的电话号码和验证码）
if __name__=='__main__':
    # accountSid, accountToken, appId, templateId
    config={
        'accountSid':'8aaf07087a331dc7017ad92a25cb33cb',
        'accountToken':'895fc86f9cec4525b9fedaf849e12d41',
        'appId':'8aaf07087a331dc7017ad92a26c433d1',
        'templateId':'1'
    }
    yun=YunTongXin(**config)
    res=yun.run('18181967801','20011016')
    print(res)



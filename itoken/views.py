from django.shortcuts import render
from django.http import JsonResponse
import json
from users.models import Usersinfo
from django.conf import settings
import hashlib
import time
import jwt

# Create your views here.

def login(request):
    return render(request,'login.html')
# 登陆
def tokens(request):
    if request.method!='POST':
        result={'code':10200,'error':'请使用POST请求'}
        return JsonResponse(result)
    json_str=request.body
    json_obj=json.loads(json_str)
    username=json_obj['username']
    password=json_obj['password']
    # 校验用户名和密码
    try:
        user=Usersinfo.objects.get(username=username)
    except Exception as e:
        result={'code':10201,'error':'用户名或密码不正确'}
        return JsonResponse(result)
    p_m=hashlib.md5()
    p_m.update(password.encode())
    if p_m.hexdigest()!=user.password:
        result={'code':10202,'error':'用户名或密码不正确'}
        return JsonResponse(result)
    # 记录会话状态
    token=make_token(username)
    result={'code':200,'username':username,'data':{'token':token}}
    return JsonResponse(result)

# 用于生成token
def make_token(username,expire=3600*24):
    # 需要到settings中去配置key
    key=settings.JWT_TOKEN_KEY
    new_t=time.time()
    payload_data={'username':username,'exp':new_t+expire}
    # 生成的jwt是字节串
    return jwt.encode(payload_data,key,algorithm='HS256')
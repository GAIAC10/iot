# 登陆装饰器

# 装饰器格式：
# def 装饰器名(视图函数):
#     def 内部函数名(request,*args,**kwargs):
#         return 视图函数(request,*args,**kwargs)
#     return 内部函数名
from django.http import JsonResponse
import jwt
from django.conf import settings
from users.models import Usersinfo


def logging_check(func):
    def wrap(request,*args,**kwargs):
        # 获取token:request.META.get('HTTP_请求头中的key（必须大写）')
        token=request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result={'code':403,'error':'Please login'}
            return JsonResponse(result)
        # 检验token(jwt)
        try:
            res=jwt.decode(token,settings.JWT_TOKEN_KEY)
        except Exception as e:
            print('jwt decode error is %s'%(e))
            result={'code':403,'error':'Please login'}
            return JsonResponse(result)
        # 因为有 class A;a=A();a.name=yukang （在python中操作 对象）[request是与视图函数唯一沟通的桥梁且是 对象]
        # 获取登陆用户
        username=res['username']
        user=Usersinfo.objects.get(username=username)
        # 自定义request的属性
        request.myuser=user
        return func(request,*args,**kwargs)
    return wrap

def get_user_by_request(request):
    # 尝试性获取登陆用户
    # return UserProfile obj or None
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res=jwt.decode(token,settings.JWT_TOKEN_KEY)
        # 如果decode报错
    except Exception as e:
        return None
    username=res['username']
    user=Usersinfo.objects.get(username=username)
    return user

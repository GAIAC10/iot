from django.core.cache import cache
from .logging_dec import get_user_by_request


# 普通装饰器模板（但是参数是整个视图函数，不能是某一个单独的参数）
# def 装饰器名(视图函数):
#     def 内部函数名(request,*args,**kwargs):
#         return 视图函数(request,*args,**kwargs)
#     return 内部函数名
# 参数装饰器模板（在该def外再定义一个def）
# def 装饰器名（参数）
#     def _装饰器名(视图函数):
#         def 内部函数名(request,*args,**kwargs):
#             return 视图函数(request,*args,**kwargs)
#         return 内部函数名
#     return _装饰器名

# 可传参的装饰器
def cache_set(expire):
    def _cache_set(func):
        def wrapper(request,*args,**kwargs):
            # 区分场景-只做列表页
            if 't_id' in request.GET:
                return func(request,*args,**kwargs)

            # 生成出 正确的[访客访问 和 博主访问] cache key
            # 从get_user_by_request获取到的用户都是visiter
            visitor_user=get_user_by_request(request)
            visitor_username=None
            if visitor_user:
                visitor_username=visitor_user.username
            # kwargs['author_id']：因为上一层def是传的参数是整个视图函数：def get(self,request,author_id)，有另一个参数author_id，用kwargs['author_id']来取
            author_username=kwargs['author_id']
            print('visitor is %s'%(visitor_username))
            print('author is %s'%(author_username))
            # 获取url来生成cache key
            full_path=request.get_full_path()
            if visitor_username==author_username:
                cache_key='topics_cache_self_%s'%(full_path)
            else:
                cache_key='topics_cache_%s'%(full_path)
            print('cache_key is %s'%(cache_key))

            # ---判断是否有缓存，有缓存则直接返回---
            res=cache.get(cache_key)
            if res:
                print('---cache in---')
                return res

            # 执行视图
            res=func(request,*args,**kwargs)

            # 存储缓存 cache对象/set/get
            cache.set(cache_key,res,expire)

            # 返回响应
            return res
        return wrapper
    return _cache_set
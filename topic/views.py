from django.shortcuts import render,HttpResponse
from django.views import View
from topic.models import Topic
from django.utils.decorators import method_decorator
from tools.cache_dec import cache_set
from users.models import Usersinfo
from django.http import JsonResponse
from tools.logging_dec import get_user_by_request, logging_check
import json
from django.core.cache import cache
from message.models import Message

# Create your views here.
def list_view(request,author_id):
    return render(request,'list.html')

def release_view(request,username):
    return render(request,'release.html')

def detail_view(request,username,t_id):
    return render(request,'detail.html')

class TopicViews(View):
    # 在下方的post中会用到
    # 清除cache
    def clear_topics_caches(self,request):
        # 取出不带查询字符串的url
        # 格式
        # cache_key is topics_cache_/v1/topics/xxx
        path=request.path_info
        cache_key_qian=['topics_cache_','topics_cache_self_']
        cache_key_hou=['','?category=tec','?category=no-tec']
        all_key=[]
        for key_qian in cache_key_qian:
            for key_hou in cache_key_hou:
                all_key.append(key_qian+path+key_hou)
        print('clear caches is',all_key)
        cache.delete_many(all_key)

    # is_self用于判断访问者是不是博主自己
    def make_topic_res(self, author, author_topic, is_self):

        if is_self:
            # 博主访问自己的
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
        else:
            # 游客访问
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
            last_topic = Topic.objects.filter(id_lt=author_topic.id, author=author, limit='public').last()

        next_id = next_topic.id if next_topic else None
        next_title = next_topic.title if next_topic else ''
        last_id = last_topic.id if last_topic else None
        last_title = last_topic.title if last_topic else ''

        # 留言功能开始\\\

        # 关联留言和回复
        all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')

        msg_list = []
        rep_dic = {}
        m_count = 0
        for msg in all_messages:
            if msg.parent_message:
                # 回复
                # .setdefault：在有d['belong_to']时，则将d['belong_to']的value作为值传入s_dict的key，并将s_dict的value设为[]，反之则不执行.setdefault方法
                rep_dic.setdefault(msg.parent_message, [])
                rep_dic[msg.parent_message].append({'msg_id': msg.id, 'publisher': msg.publisher.nickname,
                                                    'publisher_avatr': str(msg.publisher.avatar),
                                                    'content': msg.content,
                                                    'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                # 留言
                m_count += 1
                msg_list.append({'id': msg.id, 'content': msg.content, 'publisher': msg.publisher.nickname,
                                 'publisher_avatar': str(msg.publisher.avatar),
                                 'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'), 'reply': []})

        # 拼接成"messages": [],在[]中包含'id', 'content','publisher', 'publisher_avatar','created_time', 'reply';'reply'的数据是从rep_dic = {}中得来的
        for m in msg_list:
            if m['id'] in rep_dic:
                m['reply'] = rep_dic[m['id']]

        #         '''
        #         {
        #         "code":200,
        #         "data":{
        #         "nickname":"guoxiaonao",
        #         "title":"我的第一次",
        #         "category":"tec",
        #         "created_time":"2019-06-03 10:08:09",
        #         "content":"<p>我的第一次，哈哈哈哈哈<br></p>",
        #         "introduce":"我的第一次，哈哈哈哈哈",
        #         "author":"guoxiaonao",
        #         "next_id":2,
        #         "next_title":"我的第二次",
        #         "last_id":null,
        #         "last_title":null,
        #         "messages":[],
        #         "messages_count":0
        #         }
        #         }
        #         '''

        # 留言功能结束\\\

        # 生成内容
        res = {'code': 200, 'data': {}}
        res['data']['nickname'] = author.nickname
        res['data']['title'] = author_topic.title
        res['data']['category'] = author_topic.category
        res['data']['created_time'] = author_topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
        res['data']['content'] = author_topic.content
        res['data']['introduce'] = author_topic.introduce
        res['data']['author'] = author.nickname
        res['data']['last_id'] = last_id
        res['data']['last_title'] = last_title
        res['data']['next_id'] = next_id
        res['data']['next_title'] = next_title
        res['data']['messages'] = msg_list
        res['data']['messages_count'] = m_count
        return res

    # 返回api网站文档所需要的字典
    def make_topics_res(self,author,author_topics):
        # topics中,一个[]表示一个文章
        # {content: "<p>呵呵呵呵呵呵呵呵呵呵呵呵呵呵或</p><p><br></p>", content_text: "呵呵呵呵呵呵呵呵呵呵呵呵呵呵或", limit: "public",…}
        # {'code':200,'data':{'nickname':'abc','topics':[{'id':1,'title':'a','catagroy':'tec','created_time':'2018-09-03 10:30:20','introduce':'aaa','author':'abc'}]}}
        # 上面的author是nickname
        res={'code':200,'data':{}}
        topics_res=[]
        for topic in author_topics:
            d={}
            d['id']=topic.id
            d['title']=topic.title
            d['category']=topic.category
            # 自定义时间格式
            d['created_time']=topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['introduce']=topic.introduce
            d['author']=author.nickname
            topics_res.append(d)
        # 表示的是res['data']中的['topics']
        res['data']['topics']=topics_res
        res['data']['nickname']=author.nickname
        return res

    # 发表文章
    # 装饰器（每发表一篇文章，就清除cache）
    @method_decorator(logging_check)
    def post(self,request,author_id):
        author=request.myuser
        # {"content":"<p>hahahahahahaha</p>","content_text":"hahahahahahaha","limit":"public","title":"fun","category":"tec"}
        # 取出前端数据
        json_str=request.body
        json_obj=json.loads(json_str)
        title=json_obj['title']
        content=json_obj['content']
        content_text=json_obj['content_text']
        introduce=content_text[:30]
        limit=json_obj['limit']
        category=json_obj['category']
        if limit not in ['public','private']:
            result={'code':10300,'error':'The limit error'}
            return JsonResponse(result)
        # 建立topic数据
        Topic.objects.create(title=title,content=content,limit=limit,category=category,introduce=introduce,author=author)

        # 删除cache数据
        self.clear_topics_caches(request)

        return JsonResponse({'code':200})


    # 查看博主的信息（博主或游客）
    @method_decorator(cache_set(30))
    def get(self,request,author_id):
        print('-----view in -----')
        # 显示个人博客信息的时候，游客也可以观看你的blog
        # 但是在本人和游客查看自己的blog的时候，blog会输出不同的功能
        # 本人：/v1/topics/xxx
        # 访问者：/v1/topics
        try:
            author=Usersinfo.objects.get(username=author_id)
        except Exception as e:
            result={'code':10301,'error':'The author is not existed'}
            return JsonResponse(result)
        visitor=get_user_by_request(request)
        visitor_username=None
        if visitor:
            visitor_username=visitor.username
        # 从网站的网址上取数据
        t_id=request.GET.get('t_id')
        # /v1/topics/xxx?t_id=xxx
        if t_id:
            # 获取指定文章
            t_id=int(t_id)
            is_self=False
            if visitor_username==author_id:
                is_self=True
                try:
                    author_topic=Topic.objects.get(id=t_id,author_id=author_id)
                except Exception as e:
                    result={'code':10302,'error':'No topics'}
                    return JsonResponse(result)
            else:
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id,limit='public')
                except Exception as e:
                    result={'code':10303,'error':'No topics'}
                    return JsonResponse(result)
            res=self.make_topic_res(author,author_topic,is_self)
            return JsonResponse(res)
        else:
            # 获取文章列表
            # /v1/topics/xxx
            # /v1/topics/xxx?category=[tec|no-tec]·
            category=request.GET.get('category')
            if category in ['tec','no-tec']:
                if visitor_username==author_id:
                    # 博主访问自己的博客
                    author_topics=Topic.objects.filter(author_id=author_id,category=category)
                else:
                    author_topics=Topic.objects.filter(author_id=author_id,limit='public',category=category)
            else:
                if visitor_username==author_id:
                    # 博主访问自己的博客
                    author_topics = Topic.objects.filter(author_id=author_id)
                else:
                    author_topics = Topic.objects.filter(author_id=author_id, limit='public')
            res=self.make_topics_res(author,author_topics)
            # print(res)
            return JsonResponse(res)

    def delete(request,blog_delete_username,blog_delete_id):
        print(blog_delete_username)
        print(blog_delete_id)
        return HttpResponse('aaa')

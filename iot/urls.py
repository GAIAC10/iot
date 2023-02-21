"""iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
from itoken import views as itoken_views
from . import views as iot_views
from topic import views as topic_views


urlpatterns = [
    # 都是主界面
    path('',iot_views.index),
    path('index',iot_views.index),

    path('admin/', admin.site.urls),

    # def->render register函数
    path('register', user_views.register),
    # post->register数据处理
    path('users', user_views.UsersViews.as_view()),
    # 分布式路由
    path('usersdown/', include('users.urls')),
    # post->login数据处理
    path('itokens', itoken_views.tokens),
    # def->render login函数
    path('login_', itoken_views.login),
    # def->render list函数
    path('<str:author_id>/topics',topic_views.list_view),
    # 分布式路由
    path('topics/',include('topic.urls')),
    # def->render release函数
    path('<str:username>/topics/release',topic_views.release_view),
    # def->render change_info函数
    path('<str:username>/change_info',user_views.change_info),
    # def->render change_password函数 安全设置
    path('<str:username>/change_password',user_views.change_password),
    # def->render datail函数
    path('<str:username>/topics/detail/<str:t_id>',topic_views.detail_view),
    # def->render about函数 关于我
    path('<str:username>/info', user_views.about),
    # 分布式路由
    path('messages/', include('message.urls')),

    # art-Template(js插件:加载更多)
    path('test',iot_views.test),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


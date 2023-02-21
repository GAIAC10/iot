from django.db import models
import random

def default_sign():
    signs=['001','002','003']
    return random.choice(signs)

class Usersinfo(models.Model):
    username=models.CharField(max_length=11,verbose_name='用户名',primary_key=True)
    nickname=models.CharField(max_length=30,verbose_name='昵称')
    password=models.CharField(max_length=32,verbose_name='密码')
    email=models.EmailField(verbose_name='邮箱')
    phone=models.CharField(max_length=11,verbose_name='电话号码')
    # models.ImageField(头像)和models.FileField（文件）相似（前者继承于后者）
    avatar=models.ImageField(upload_to='avatar',null=True,verbose_name='头像')
    sign=models.CharField(max_length=50,verbose_name='个人签名',default=default_sign)
    info=models.CharField(max_length=150,verbose_name='个人简介',default='')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
       db_table='users_info'



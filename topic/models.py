from django.db import models
from users.models import Usersinfo

# Create your models here.

class Topic(models.Model):
    title=models.CharField(max_length=50,verbose_name='文章标题')
    category=models.CharField(max_length=20,verbose_name='文章分类')
    limit=models.CharField(max_length=20,verbose_name='文章权限')
    introduce=models.CharField(max_length=90,verbose_name='文章简介')
    content=models.TextField(verbose_name='文章内容')
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time=models.DateTimeField(verbose_name='更新时间',auto_now=True)
    # on_delete=models.CASCADE表示auther被删除的话，Topic也会被删
    author=models.ForeignKey(Usersinfo,on_delete=models.CASCADE)

    class Meta:
       db_table='topic_info'

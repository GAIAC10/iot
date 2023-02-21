# Generated by Django 3.2.11 on 2023-02-21 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('category', models.CharField(max_length=20, verbose_name='文章分类')),
                ('limit', models.CharField(max_length=20, verbose_name='文章权限')),
                ('introduce', models.CharField(max_length=90, verbose_name='文章简介')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.usersinfo')),
            ],
            options={
                'db_table': 'topic_info',
            },
        ),
    ]

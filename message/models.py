from django.db import models
from topic.models import Topic
from users.models import Usersinfo

# Create your models here.
class Message(models.Model):

    content = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    parent_message = models.IntegerField(verbose_name='回复的留言id')
    publisher = models.ForeignKey(Usersinfo, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
       db_table='message_info'
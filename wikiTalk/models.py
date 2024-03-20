from django.db import models

# Create your models here.
class Message(models.Model):
    username = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    pub_time = models.DateTimeField(auto_now_add=True)
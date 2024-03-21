from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TalkMessage(models.Model):
	id = models.AutoField("id", primary_key=True)
	user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
	message = models.CharField("Message", max_length=100)
	edit_time = models.DateTimeField("Edit Time", auto_now=True, auto_now_add=False)
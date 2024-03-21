from django.contrib import admin
from .models import TalkMessage
# Register your models here.

class TalkMessageAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "message", "edit_time")

admin.site.register(TalkMessage, TalkMessageAdmin)
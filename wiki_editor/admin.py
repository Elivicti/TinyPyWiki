from django.contrib import admin
from django.utils import timezone
from .models import WikiArticle, WikiArticleEditLog

# Register your models here.

class WikiArticleAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "last_editor", "last_edit_time")

	@admin.display(description="Editor")
	def last_editor(self, obj: WikiArticle):
		last_edit = WikiArticleEditLog.objects.filter(article_id=obj.id).order_by("-edit_time")[0]
		return last_edit.editor
	
	@admin.display(description="Edit Time")
	def last_edit_time(self, obj: WikiArticle):
		last_edit = WikiArticleEditLog.objects.filter(article_id=obj.id).order_by("-edit_time")[0]
		return timezone.localtime(last_edit.edit_time).strftime("%Y-%m-%d %H:%M:%S %Z")
		# return obj.last_edit.edit_time.strftime("%Y-%m-%d %H:%M:%S %Z")

class WikiArticleEditLogAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "editor", "last_edit_time", "commit_msg")

	@admin.display(description="Title")
	def title(self, obj: WikiArticleEditLog):
		return obj.article_id.title
	
	@admin.display(description="Edit Time")
	def last_edit_time(self, obj):
		return timezone.localtime(obj.edit_time).strftime("%Y-%m-%d %H:%M:%S %Z")


admin.site.register(WikiArticle, WikiArticleAdmin)
admin.site.register(WikiArticleEditLog, WikiArticleEditLogAdmin)
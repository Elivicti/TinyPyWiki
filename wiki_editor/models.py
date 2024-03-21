from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class WikiArticle(models.Model):
	id = models.AutoField("id", primary_key=True)
	title = models.CharField("title", max_length=100)
	# last_edit = models.ForeignKey(WikiArticleEditLog, verbose_name="last edit", on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Wiki Article"


class WikiArticleEditLog(models.Model):
	id = models.AutoField("id", primary_key=True)
	article_id = models.ForeignKey(WikiArticle, verbose_name="article id", on_delete=models.CASCADE)
	content = models.TextField("content")
	edit_time = models.DateTimeField("edit time", auto_now=True, auto_now_add=False)
	editor = models.ForeignKey(User, verbose_name="editor", on_delete=models.CASCADE)
	commit_msg = models.CharField("Commit message", max_length=80)

	class Meta:
		verbose_name = "Wiki Article Edit Log"


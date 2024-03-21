from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .utils import get_article_title
from .models import WikiArticle, WikiArticleEditLog

class WikiArticleForm(forms.ModelForm):
    class Meta:
        model = WikiArticle
        fields = ["title"]
    

class WikiEditorForm(forms.ModelForm):
    class Meta:
        model = WikiArticleEditLog
        fields = ["content", "commit_msg", "editor", "article_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = ""
        self.fields["commit_msg"].widget.attrs = {
            "class": "django-form-lineinput",
            "style": "width: 70%;",
            "placeholder": "Commit Message..."
        }
        
        self.fields["editor"].widget.attrs = {"type":"hidden" }
        self.fields["article_id"].widget.attrs = {"type":"hidden" }
        
    def check(self) -> bool:
        self.full_clean()
        try:
            article = self.cleaned_data["content"]
            self.title = get_article_title(article)
        except Exception as e:
            self.add_error(field=None, error=ValidationError(str(e)))
        return self.is_valid()


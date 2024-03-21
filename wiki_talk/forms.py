from django import forms
from .models import TalkMessage

class TalkMessageForm(forms.ModelForm):
	class Meta:
		model = TalkMessage
		fields = ["user", "message"]
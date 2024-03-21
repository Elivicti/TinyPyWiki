from django.shortcuts import render, redirect

from mainwiki.utils import get_section_tab

from .models import TalkMessage

from . import forms
# Create your views here.

def show_talk(request):
	if request.method == "GET":
		messages = TalkMessage.objects.filter().order_by("-edit_time")
	
	
		form = forms.TalkMessageForm(initial={"user": request.user})
		return render(request, "talk.html", {
		"hide_external_links": True,
		"talk_page": "Talk",
		"tab_sections": get_section_tab(request, None, "read", force_hide_editor=True, force_hide_history=True),
		"messages": messages,
		"var_last_edit_time": messages[0].edit_time,
		"form": form
		})
	
	form = forms.TalkMessageForm(initial={"user": request.user},data=request.POST)
	form.full_clean()
	if form.is_valid():
		form.save()
		return redirect("/talk/")


def func(request):
	request.user

	pass

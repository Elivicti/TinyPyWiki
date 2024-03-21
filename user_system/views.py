from django.shortcuts import render, redirect
from django.utils.safestring import SafeText
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

# Create your views here.


def user_login(request):
	if request.method == "GET":
		return render(request, "login.html", { "form" : forms.WikiUserLogin() })
	
	next = request.POST.get('next', '/')
	if (next == "/user/register/" or next == ""):
		next = "/"

	email = request.POST["email"]
	password = request.POST["password"]
	user_obj = User.objects.filter(email=email)
	form = forms.WikiUserLogin(data=request.POST)
	if not form.check(user_obj):
		return render(request, "login.html", { "form" : form })
	user = authenticate(request, username=user_obj[0].username, password=password)
	if user is None:
		form.add_error("password", ValidationError("Incorrect password."))
		return render(request, "login.html", { "form" : form })

	login(request, user)

	return redirect(next)

def user_logout(request):
	next_page = request.META.get("HTTP_REFERER")
	logout(request)
	return redirect(request.META.get("HTTP_REFERER"))

def register(request):
	if request.method == "GET":
		form = forms.WikiUserRegister()
		return render(request, "register.html", { "form" : form })
	
	next = request.POST.get('next', '/')
	if (next == "/user/login/" or next == ""):
		next = "/"

	form = forms.WikiUserRegister(data=request.POST)
	if form.check():
		form.save()
		user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
		login(request, user)
		return redirect(next)
	
	return render(request, "register.html", {
		"form" : form,
		"correct_error_tooltip": SafeText("<p class=\"django-form-8\">Please correct the errors below.</p>")
	})	# contains error message
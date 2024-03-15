from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import SafeText
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@csrf_exempt
def user_login(request):
	if request.method == "GET":
		print("MSG: rednering")
		return render(request, "login.html", { "form" : forms.WikiUserLogin() })
	
	email = request.POST["email"]
	password = request.POST["password"]
	user_obj = User.objects.filter(email=email)
	user = authenticate(request, username=user_obj[0].username, password=password)
	login(request, user)
	print("---------------------------")
	print("Email: {}; Password: {}".format(email, password))
	print(user)
	for obj in user_obj:
		print(obj.username)
	print("---------------------------")

	return render(request, "login.html", { "form" : forms.WikiUserLogin() })

@csrf_exempt
def register(request):
	if request.method == "GET":
		print("MSG: rendering")
		form = forms.WikiUserRegister()
		return render(request, "register.html", { "form" : form })
	
	form = forms.WikiUserRegister(data=request.POST)
	if form.check():
		form.save()
		user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
		login(request, user)
		return redirect("/")
	
	return render(request, "register.html", {
		"form" : form,
		"correct_error_tooltip": SafeText("<p class=\"django-form-8\">Please correct the errors below.</p>")
	})	# contains error message
from typing import Any, Mapping
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html


class FieldValidationError(ValidationError):
	def __init__(self, field: str, message: Any, code: str | None = None,  params: Mapping[str, Any] | None = None) -> None:
		super().__init__(message, code, params)
		self.field = field
		
class WikiUserLogin(forms.ModelForm):
	class Meta:
		model = User
		fields = ["email", "password"]
	def __init__(self, *args, **kwargs):
		
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if name == "password":
				field.widget = forms.PasswordInput()
			field.widget.attrs = {"class" : "django-form-lineinput"}

	def check(self):
		self.full_clean()
		try:
			for field in self.Meta.fields:
				if not field in self.cleaned_data.keys():
					raise FieldValidationError(field, "This field is required.")
			if not User.objects.filter(email="email").exists():
				raise FieldValidationError("email", "Unrecognized email address.")
			pass
		except FieldValidationError as err:
			self.add_error(err.field, err)
		
		return  self.is_valid()


class WikiUserRegister(forms.ModelForm):
	class Meta:
		model = User
		fields = ["email", "username", "password", "confirm_pwd"]
		help_texts = {
			"password": password_validators_help_text_html,
		}
		error_messages = {
			"username": {
				"unique" : "A user with this username already exists."
			}
		}

	confirm_pwd = forms.CharField(
		label="Password confirmation",
		widget=forms.PasswordInput(attrs={"class":"form-control"}),
		help_text="Must be the same with password."
	)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if name == "password":
				field.widget = forms.PasswordInput()
			field.widget.attrs = {"class" : "django-form-lineinput"}

	def debug_func(self):
		self.confirm_pwd.help_text
		# a = User()
		# a.username_validator
		pass

	def check(self) -> bool:
		self.full_clean()
		pwd_confirm = True
		data_keys = self.cleaned_data.keys()
		try:
			email = self.cleaned_data["email"] # why does this key exist when user doesnot input email?
			if email:
				if User.objects.filter(email=email).exists():
					raise FieldValidationError("email", "A user with this email already exists.")
			else:
				raise FieldValidationError("email", "This field is required.")

			if "password" in data_keys and "confirm_pwd" in data_keys:
				pwd = self.cleaned_data["password"]
				confirm_pwd = self.cleaned_data["confirm_pwd"]
				if not pwd == confirm_pwd:
					raise FieldValidationError("confirm_pwd", "Password not the same.")
				validate_password(self.cleaned_data["password"], self.instance)
		except FieldValidationError as err:
			pwd_confirm = False
			self.add_error(err.field, err)
		except ValidationError as err:
			pwd_confirm = False
			self.add_error("password", err)

		return self.is_valid() and pwd_confirm
	
	def save(self, commit: bool = True):
		if commit:
			self.instance.set_password(self.cleaned_data["password"])
		super().save(commit)

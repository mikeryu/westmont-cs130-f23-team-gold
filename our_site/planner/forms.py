from django import forms
from .models import Event, Profile

from django.contrib.auth.forms import User



class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)

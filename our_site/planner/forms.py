from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)


def is_user_name(user_name: str) -> None:
    matching_users = User.objects.all().filter(username__exact=user_name)
    if len(matching_users) != 1:
        raise ValidationError("'{:s}' is not an existing user.".format(user_name), code="invalid user")


class SelectUserForm(forms.Form):
    user_name = forms.CharField(max_length=150, validators=[is_user_name])


class AddInvitationForm(SelectUserForm):
    user_name = forms.CharField(label="Invite User:", max_length=150, validators=[is_user_name])


class RemoveInvitationForm(SelectUserForm):
    pass

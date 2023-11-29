from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import User
from .models import Role, Event
from .import views



class RoleForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=100)  
    amount = forms.IntegerField()

    class Meta:
        model = Role
        exclude = ("user",)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)


def is_user_name(user_name: str) -> None:
    """
    This is a utility function for determining if a string is a valid username in the database.
    If the string is a valid username, the function returns None.
    If there is no user with this username, the function raises a ValidationError.

    :param user_name:
    """
    matching_users = User.objects.all().filter(username__exact=user_name)
    if len(matching_users) != 1:
        raise ValidationError("'{:s}' is not an existing user.".format(user_name), code="invalid user")


class SelectUserForm(forms.Form):
    """
    Base class form for getting the name of a user.
    Provides validation that the name of the user actually exists in the database.
    """
    user_name = forms.CharField(max_length=150, validators=[is_user_name])


class AddInvitationForm(SelectUserForm):
    user_name = forms.CharField(label="Username:", max_length=150, validators=[is_user_name])


class RemoveInvitationForm(SelectUserForm):
    pass

from django.shortcuts import render, redirect
import django.contrib.auth.views as auth_views
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from planner.models import Profile
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


class PlannerLoginView(auth_views.LoginView):
    next_page = "/planner/dashboard/"


def newAccount(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            user = User.objects.all().filter(username__exact=user.username).get()
            login(request, user)
            return redirect('planner:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/newAccount.html', {'form': form})


def logout_view(request) -> HttpResponseRedirect:
    """
    logout_view is just an intermediate page where the user gets logged out before they are redirected to the login
    page.

    :param request: http request for the logout page.
    :return: An http redirect to the login page.
    """
    logout(request)
    return HttpResponseRedirect("/account/login")

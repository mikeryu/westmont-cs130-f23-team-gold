from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import LoginForm


def dashboard(request):
    if request.user.is_anonymous:  # User is redirected to login if they are not logged in
        return HttpResponseRedirect("/account/login/")

    template = loader.get_template('planner/dashboard.html')
    return HttpResponse(template.render({}, request))

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "planner/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    return render(request, "planner/profile.html", {"profile": profile})
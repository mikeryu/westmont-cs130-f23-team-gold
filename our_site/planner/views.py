from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import LoginForm


def dashboard(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    template = loader.get_template('planner/dashboard.html')
    return HttpResponse(template.render({}, request))


def event_creation(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    template = loader.get_template('planner/event_creation.html')
    return HttpResponse(template.render({}, request))

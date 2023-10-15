from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import LoginForm


def dashboard(request):
    template = loader.get_template('planner/dashboard.html')
    return HttpResponse(template.render({}, request))

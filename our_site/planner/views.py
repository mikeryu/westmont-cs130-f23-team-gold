from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event

from .forms import LoginForm


def dashboard(request):
    event_list = Event.objects
    name = Event.name
    context = {"name" : name, "planner_event": event_list}
    return render(request, "planner/dashboard.html", context)
    # if request.user.is_anonymous:  # User is redirected to login if they are not logged in
    #     return HttpResponseRedirect("/account/login/")

    # template = loader.get_template('planner/dashboard.html')
    # return HttpResponse(template.render({}, request))

# def event(request, name):
#     context = {"name" : name, "planner_event": Event}
#     return render(request, "dashboard.html", context)
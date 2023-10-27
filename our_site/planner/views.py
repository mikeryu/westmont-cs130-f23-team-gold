from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event

from .forms import LoginForm


def dashboard(request):
    owner = None
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    owner = request.user.profile
    invited = request.user.profile.events.invitees

    owned_event_list = Event.objects.filter(owner_id=owner)

    invited_event_list = Event.objects.filter(profile_id=invited)

    event_list = owned_event_list + invited_event_list

    

    context = {"owner" : owner, "planner_event_invitees": event_list}
    
    return render(request, "planner/dashboard.html", context)

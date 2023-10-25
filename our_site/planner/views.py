from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import django.forms as forms

from .forms import LoginForm


class DashboardFilterAllEvents(forms.Form):
    pass


class DashboardFilterMyEvents(forms.Form):
    pass


class DashboardFilterInvitedEvents(forms.Form):
    pass


def dashboard(request):
    if request.user.is_anonymous:  # User is redirected to login if they are not logged in
        return HttpResponseRedirect("/account/login/")

    if request.method == "POST":
        template = loader.get_template('planner/dashboard.html')

        if "filter_all_events" in request.POST:
            filter_value = "All Events"
        elif "filter_my_events" in request.POST:
            filter_value = "My Events"
        elif "filter_invited_events" in request.POST:
            filter_value = "Invited Events"
        else:
            raise Exception("unknown post provided")

        return HttpResponse(template.render(
            {
                "filter_value": filter_value,
                "AllEventsButton": DashboardFilterAllEvents(),
                "MyEventsButton": DashboardFilterMyEvents(),
                "InvitedEventsButton": DashboardFilterInvitedEvents(),
            },
            request
        ))

    template = loader.get_template("planner/dashboard.html")
    return HttpResponse(template.render(
        {
            "filter_value": "All Events",
            "AllEventsButton": DashboardFilterAllEvents(),
            "MyEventsButton": DashboardFilterMyEvents(),
            "InvitedEventsButton": DashboardFilterInvitedEvents(),
        },
        request
    ))

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
import django.forms as forms
from django.shortcuts import render

from .models import Event, Profile


class DashboardFilterAllEvents(forms.Form):
    pass


class DashboardFilterMyEvents(forms.Form):
    pass


class DashboardFilterInvitedEvents(forms.Form):
    pass


def dashboard(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    owner = request.user.profile
    event_list = Event.objects.filter(owner_id=owner)

    if request.method == "POST":
        template = loader.get_template('planner/dashboard.html')

        if "filter_all_events" in request.POST:
            filter_value = "All Events"

            owned_events_list = []

            invited_list = []
            for invitedEvent in Event.objects.all():
                if invitedEvent.invitees.contains(request.user.profile):
                    invited_list.append(invitedEvent)

            for events in Event.objects.filter(owner_id=owner):
                if events in invited_list:
                    owned_events_list = owned_events_list
                else:
                    owned_events_list.append(events)

            event_list = owned_events_list + invited_list

        elif "filter_my_events" in request.POST:
            filter_value = "My Events"
            owner = request.user.profile
            event_list = Event.objects.filter(owner_id=owner)

        elif "filter_invited_events" in request.POST:
            filter_value = "Invited Events"
            event_list = []
            for invitedEvent in Event.objects.all():
                if invitedEvent.invitees.contains(request.user.profile):
                    event_list.append(invitedEvent)

        else:
            raise Exception("unknown post provided")

        return HttpResponse(template.render(
            {
                "filter_value": filter_value,
                "AllEventsButton": DashboardFilterAllEvents(),
                "MyEventsButton": DashboardFilterMyEvents(),
                "InvitedEventsButton": DashboardFilterInvitedEvents(),
                "event_list": event_list,
                "owner": owner,
            },
            request
        ))

    template = loader.get_template("planner/dashboard.html")
    return HttpResponse(template.render(
        {
            "filter_value": "My Events",
            "AllEventsButton": DashboardFilterAllEvents(),
            "MyEventsButton": DashboardFilterMyEvents(),
            "InvitedEventsButton": DashboardFilterInvitedEvents(),
            "event_list": event_list,
            "owner": owner,
        },
        request
    ))


class EventCreationForm(forms.Form):
    event_name = forms.CharField(label="Event Name:", max_length=30, required=True)
    event_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label="Event Date (dd/mm/yy hh:mm):",
                                     required=True)
    event_description = forms.CharField(label="Event Description:", max_length=200, required=True)
    event_location = forms.CharField(label="Event Location:", max_length=50, required=True)


def event_creation(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    if request.method == "GET":
        template = loader.get_template("planner/event_creation.html")
        event_creation_form = EventCreationForm()
        return HttpResponse(template.render({"event_creation_form": event_creation_form}, request))
    elif request.method == "POST":
        # It is acceptable to shove the data from this post into one form because currently only one form
        # leads to this page
        event_creation_form = EventCreationForm(request.POST)
        # If the form is valid, save the new event and move to it's editing page
        # otherwise, just redisplay the form with its errors
        if event_creation_form.is_valid():
            event = Event(
                owner=request.user.profile,
                name=event_creation_form.cleaned_data["event_name"],
                date=event_creation_form.cleaned_data["event_date"],
                description=event_creation_form.cleaned_data["event_description"],
                location=event_creation_form.cleaned_data["event_location"],
            )
            event.save()
            return HttpResponseRedirect("/planner/{:d}/edit_event".format(event.id))
        else:
            template = loader.get_template("planner/event_creation.html")
            return HttpResponse(template.render({"event_creation_form": event_creation_form}, request))


def edit_event(request, event_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    event_getter = Event.objects.all().filter(id__exact=event_id)
    if len(event_getter) == 0:  # If the event to "edit" doesn't exist, redirect to dashboard
        return HttpResponseRedirect("/account/dashboard")
    event = Event.objects.all().filter(id__exact=event_id).get()  # otherwise, store it here

    user_profile_id = request.user.profile.id
    owner_profile_id = event.owner_id
    if user_profile_id != owner_profile_id:  # If the user does not own this event, they can't edit it
        return HttpResponseRedirect("/account/dashboard")

    template = loader.get_template("planner/edit_event.html")
    basic_details = EventCreationForm()
    basic_details.event_name = event.name
    basic_details.event_date = event.date
    basic_details.event_description = event.description
    basic_details.event_location = event.location
    return HttpResponse(
        template.render(
            {
                "basic_details": basic_details,
                "form_action": "planner:{:d}/edit_event/".format(event_id),
            },
            request,
        )
    )

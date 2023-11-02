from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
import django.forms as forms
<<<<<<< HEAD
from .models import Event
from django.shortcuts import render



def dashboard(request):
    
    owner = request.user.profile
    event_list=[]
    class DashboardFilterAllEvents(forms.Form):
        pass

    class DashboardFilterMyEvents(forms.Form):
        pass

    class DashboardFilterInvitedEvents(forms.Form):
        pass

    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
       return HttpResponseRedirect("/account/login/")
=======
from django.shortcuts import render

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
>>>>>>> b5246a2 (Dashboard Views with Filtering (#43))

    if request.method == "POST":
        template = loader.get_template('planner/dashboard.html')
        

        if "filter_all_events" in request.POST:
            filter_value = "All Events"
<<<<<<< HEAD
            owned_events_list = []
=======

            owned_events_list = []

>>>>>>> b5246a2 (Dashboard Views with Filtering (#43))
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
<<<<<<< HEAD
            owned_events_list = []
            invited_list = []
            for events in Event.objects.filter(owner_id=owner):
                if events in invited_list:
                    owned_events_list = owned_events_list
                else:
                    owned_events_list.append(events) 
            event_list = owned_events_list + invited_list
            

        elif "filter_invited_events" in request.POST:
            filter_value = "Invited Events"
=======
            owner = request.user.profile
            event_list = Event.objects.filter(owner_id=owner)

        elif "filter_invited_events" in request.POST:
            filter_value = "Invited Events"
            event_list = []
>>>>>>> b5246a2 (Dashboard Views with Filtering (#43))
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
<<<<<<< HEAD
                "event_list": event_list,
                "owner": owner,
=======
                "event_list" : event_list,
                "owner" : owner,

>>>>>>> b5246a2 (Dashboard Views with Filtering (#43))
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
            "event_list" : event_list,
            "owner" : owner,
        },
        request
    ))


class EventCreationForm(forms.Form):
    event_name = forms.CharField(label="Event Name:", max_length=30, required=True)
    event_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label="Event Date (dd/mm/yy hh:mm):", required=True)
    event_description = forms.CharField(label="Event Description:", max_length=200, required=True)
    event_location = forms.CharField(label="Event Location:", max_length=50, required=True)
    event_invitees_emails = forms.CharField(label="Invitees (comma delimited emails):", required=True)
    event_roles = forms.CharField(label="Roles (comma separated zipped list of roles and quantities):", required=True)


def event_creation(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    if request.method == "GET":
        template = loader.get_template('planner/event_creation.html')
        form = EventCreationForm()
        return HttpResponse(template.render({"form": form}, request))


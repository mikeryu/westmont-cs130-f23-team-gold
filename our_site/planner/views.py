from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
import django.forms as forms



class DashboardFilterAllEvents(forms.Form):
    pass


class DashboardFilterMyEvents(forms.Form):
    pass


class DashboardFilterInvitedEvents(forms.Form):
    pass


def dashboard(request):

    owner = None
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    owner = request.user.profile
    invited = request.user.profile.events

    owned_event_list = Event.objects.filter(owner_id=owner)
    invited_event_list = Event.objects.filter(profile_id=invited)
    event_list = owned_event_list + invited_event_list

    context = {"owner" : owner, "planner_event_invitees": event_list}
    
    return render(request, "planner/dashboard.html", context)

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


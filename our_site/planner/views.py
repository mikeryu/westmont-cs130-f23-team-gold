from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
import django.forms as forms
from django.contrib import messages

from .models import Event, User
from .forms import AddInvitationForm, RemoveInvitationForm
from .forms import RoleForm
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


class EventBasicDetails(forms.Form):
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
        event_creation_form = EventBasicDetails()
        return HttpResponse(template.render({"event_creation_form": event_creation_form}, request))
    elif request.method == "POST":
        # It is acceptable to shove the data from this post into one form because currently only one form
        # leads to this page
        event_creation_form = EventBasicDetails(request.POST)
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


def event_specific_credentials(request, event_id) -> HttpResponseRedirect | Event:
    """
    This is a utility function that allows you to tell if a user has logged in and is the owner of
    an event. If this is the case, the Event record will be returned, and if not an HttpResponseRedirect.

    :param request: The HTTP request for a page
    :param event_id: the id of the event in the url
    :return: If the user is logged in as the owner of an event with the id event_id, that Event.
             Otherwise, an HttpResponseRedirect to the login page if the user isn't logged in,
             and an HttpResponseRedirect to the user's dashboard if they do not own the event
             or if the event does not exist.
    """
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

    return event


def edit_event(request, event_id: int) -> HttpResponse:
    """
    This view provides a way for user to edit the basic details of an event they own (the name, date, description,
    and location). Users are verified as the owners of the event using event_specific_credentials.

    :param request: The Http request for a page
    :param event_id: the id of the event that the user wants to edit
    :return: An HttpResponse of the rendered template planner/edit_event.html
    """
    event = event_specific_credentials(request, event_id)
    if isinstance(event, HttpResponseRedirect):
        return event

    # If a get, give the template to edit an event.
    # If a post, try to validate the form and save information,
    # and then give back the template to edit the event.
    template = loader.get_template("planner/edit_event.html")
    match request.method:
        case "GET":
            pass
        case "POST":
            # It is acceptable to shove the data from this post into one form because currently only one form
            # leads to this page
            posted_details = EventBasicDetails(request.POST)
            # If the form is valid, update the event and reload the page
            # otherwise, just redisplay the form with its errors
            if posted_details.is_valid():
                event.name = posted_details.cleaned_data["event_name"]
                event.date = posted_details.cleaned_data["event_date"]
                event.description = posted_details.cleaned_data["event_description"]
                event.location = posted_details.cleaned_data["event_location"]
                event.save()

    basic_details = EventBasicDetails(initial={
        "event_name": str(event.name),
        "event_date": str(event.date),
        "event_description": str(event.description),
        "event_location": str(event.location),
    })
    return HttpResponse(
        template.render(
            {
                "basic_details": basic_details,
            },
            request
        )
    )


def event_home(request, event_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")
<<<<<<< HEAD
=======

    event = Event.objects.all().filter(id__exact=event_id).get()
>>>>>>> ba42354 (Adding things to backend roles logic  (#73))

    event = Event.objects.all().filter(id__exact=event_id).get()
    #role= Role.objects().filter()
    user_profile_id = request.user.profile.id
    owner_profile_id = event.owner_id
    invitee_profile_ids = event.invitees.values_list('id', flat=True)

    roles_list=[]
    for role in event.roles.all():
        roles_list.append(role)

    if user_profile_id != owner_profile_id and user_profile_id not in invitee_profile_ids:
        return HttpResponseRedirect("/account/dashboard")

    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    return HttpResponse(
        render(request, 'planner/event_home.html', {'event': event ,"roles_list": roles_list} )
    )


def invitations(request, event_id: int) -> HttpResponse:
    """
    The "invitations" view provides a page where the owner of an event may add or remove users from the guest list.
    Uses event_specific_credentials for authentication that the user owns the event.

    :param request: the Http request for a page
    :param event_id: the id of the event that someone wants to edit
    :return: An HttpResponse of the rendered template planner/event_modify_invitees.html
    """
    event = event_specific_credentials(request, event_id)
    if isinstance(event, HttpResponseRedirect):
        return event

    match request.method:
        case "GET":
            pass
        case "POST":
            if "add" in request.POST:
                form = AddInvitationForm(request.POST)
                # If the name they type in is a user on record, add their profile as an invitee
                # Otherwise throw the form back at them with a message that they did not ender the name
                # of a registered user
                if form.is_valid():
                    # Safe to get directly because user existence has been validated by the form validation
                    matching_user = User.objects.all().filter(username__exact=form.cleaned_data["user_name"]).get()
                    event.invitees.add(matching_user.profile)
                    event.save()
                else:
                    messages.info(request, "'{:s}' is not a registered user.".format(form.data["user_name"]))
            elif "remove" in request.POST:
                form = RemoveInvitationForm(request.POST)
                # If the name they type in is a user on record, remove their profile from invitations
                # Otherwise throw the form back at them with any errors
                if form.is_valid():
                    matching_user = User.objects.all().filter(username__exact=form.cleaned_data["user_name"]).get()
                    event.invitees.remove(matching_user.profile)
                    event.save()
            else:
                raise Exception("That's not a valid POST...")

    current_invitee_names = sorted([invitee.user.username for invitee in event.invitees.all()])
    current_invitees = [
        {
            "name": name,
            "uninvite_form": RemoveInvitationForm(initial={"user_name": name}),
        }
        for name in current_invitee_names
    ]

    template = loader.get_template("planner/event_modify_invitees.html")
    return HttpResponse(
        template.render(
            {
                "messages": messages.get_messages(request),
                "invitees": current_invitees,
                "invite_form": AddInvitationForm(),
                "event_edit_page": "/planner/{:d}/edit_event/".format(event_id),
            },
            request,
        )
    )


class RoleDetails(forms.Form):
    role_name = forms.CharField(max_length=30)


def addRoles(request):
<<<<<<< HEAD
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    if request.method == "GET":
        template = loader.get_template("planner/addRoles.html")
        addRoles_form = RoleForm()
        return HttpResponse(template.render({"addRoles_form": addRoles_form}, request))
    elif request.method == "POST":
        addRoles_form = RoleForm(request.POST)
=======
   
   
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")
<<<<<<< HEAD
    if request.method=="GET":
        template=loader.get_template("planner/addRoles.html")
        addRoles_form=RoleForm()
        return HttpResponse(template.render({"addRoles_form": addRoles_form},request))
    elif request.method=="POST":    
        addRoles_form=RoleForm(request.POST)
>>>>>>> 778076c (sprint 4)
=======

    if request.method == "GET":
        template = loader.get_template("planner/addRoles.html")
        addRoles_form = RoleForm()
        return HttpResponse(template.render({"addRoles_form": addRoles_form}, request))
    elif request.method == "POST":
        addRoles_form = RoleForm(request.POST)
>>>>>>> ba42354 (Adding things to backend roles logic  (#73))
        if addRoles_form.is_valid():
            role = addRoles_form.save(commit=False)
            role.user = request.user
            role.save()

<<<<<<< HEAD
<<<<<<< HEAD
        addRoles_form = RoleForm()
=======
        addRoles_form=RoleForm()
        return render(request, "planner/addRoles.html", {"addRoles_form":addRoles_form})
>>>>>>> 778076c (sprint 4)

    else:
<<<<<<< HEAD
        template = loader.get_template("planner/dashboard.html")
        return HttpResponse(template.render({"RoleDetails": RoleDetails}, request))
=======
        template=loader.get_template("planner/dashboard/html")
        return HttpResponse(template.render({"RoleDetails": RoleDetails},request))
    
    

>>>>>>> 778076c (sprint 4)
=======
        addRoles_form = RoleForm()

        return render(request, "planner/addRoles.html", {"addRoles_form": addRoles_form})
    else:
        template = loader.get_template("planner/dashboard.html")
        return HttpResponse(template.render({"RoleDetails": RoleDetails}, request))
>>>>>>> ba42354 (Adding things to backend roles logic  (#73))

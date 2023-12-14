from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
import django.forms as forms
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

from .models import Event, User, Profile, Role
from .forms import AddInvitationForm, RemoveInvitationForm
from .forms import RoleForm

from notifications.notify_email import send_notification


def dashboard(request) -> HttpResponse:
    """
    dashboard is the central "hub" of our website, where users can view all the events that they have created or have
    been invited to. The dashboard is actually made up of four slightly different html templates.
    Each template has a different "activated" button on the menu of 4 buttons to indicate what the shown events
    are being filtered by (all events, owned events, attending, and invited).

    :param request: The HTTP request for a page.
    :return: If the user is not logged in, an HTTP redirect to the login page.
             Otherwise, one of the four rendered templates corresponding to each of the filters.
    """
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    owner = request.user.profile
    # Get the full url, because the last part of the url is the value by which to filter events
    filter_value = request.build_absolute_uri().split("/")[-2]

    match filter_value:
        case "allevents":
            template = loader.get_template("planner/dash_allevents.html")

            owned_events_list = list(Event.objects.all().filter(owner=owner))
            invited_list = list(Event.objects.all().filter(invitees__in=[owner]))
            attending_list = list(Event.objects.all().filter(attendees__in=[owner]))

            event_list = owned_events_list + invited_list + attending_list
        case "myevents":
            template = loader.get_template("planner/dash_myevents.html")
            owner = request.user.profile
            event_list = list(Event.objects.filter(owner_id=owner))
        case "accevents":
            template = loader.get_template("planner/dash_accevents.html")
            owner = request.user.profile
            event_list = list(Event.objects.all().filter(attendees__in=[owner]))
        case "invevents":
            template = loader.get_template("planner/dash_invevents.html")
            event_list = list(Event.objects.all().filter(invitees__in=[owner]))
        case _:
            return HttpResponseRedirect("/planner/dashboard/allevents")

    return HttpResponse(template.render(
        {
            "event_list": event_list,
            "owner": owner,
        },
        request
    ))


class EventBasicDetails(forms.Form):
    event_name = forms.CharField(label="Event Name:", max_length=30, required=True)
    event_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label="Event Date (yyyy-mm-dd):",
                                     required=True)
    event_description = forms.CharField(
        label="Event Description:",
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={'class': 'event-description', 'style': 'width: 763px; height: 172px'}),
    )
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
            if (username := request.user.username).endswith("@westmont.edu"):
                send_notification(username, "Your new event is live!", "Your event '{:s}' has been created!\n"
                                                                       "Go invite people now.".format(event.name))
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
                return HttpResponseRedirect("/planner/event_owned/{:d}/".format(event.id))

    if request.method == "POST":
        if "Add Invitees" in request.POST:
            return HttpResponseRedirect("/planner/{:d}/invitations/".format(event.id))

        # if "Save Changes" in request.POST:
        #     event.save()
        #     return HttpResponseRedirect("/planner/event_owned/{:d}/".format(event.id))

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
                "event_id": event.id,
            },
            request
        )
    )


def event_home_owned(request, event_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    event = Event.objects.all().filter(id__exact=event_id).get()
    invitees = event.invitees.all()
    attendees = event.attendees.all()

    user_profile_id = request.user.profile.id
    owner_profile_id = event.owner_id
    invitee_profile_ids = event.invitees.values_list('id', flat=True)
    roles_list = list(event.roles.all())

    if user_profile_id != owner_profile_id and user_profile_id not in invitee_profile_ids:
        return HttpResponseRedirect("/planner/dashboard")

    if user_profile_id != owner_profile_id:
        return HttpResponseRedirect("/planner/event/{:d}/".format(event.id))

    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    if request.method == "POST":
        if "Edit Event" in request.POST:
            return HttpResponseRedirect("/planner/{:d}/edit_event".format(event.id))

    return HttpResponse(
        render(
            request,
            'planner/event_home_owned.html',
            {
                'event': event,
                'invitees': invitees,
                'attendees': attendees,
                "roles_list": roles_list,
                "edit_link": "/planner/{:d}/edit_event".format(event_id),
            }
        )
    )


def event_home(request, event_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    event = Event.objects.all().filter(id__exact=event_id).get()
    invitees = event.invitees.all()
    attendees = event.attendees.all()

    profile_id = request.user.profile.id
    profile = Profile.objects.all().filter(id=profile_id).get()

    user_profile_id = request.user.profile.id
    owner_profile_id = event.owner_id
    invitee_profile_ids = event.invitees.values_list('id', flat=True)
    attendee_profile_ids = event.attendees.values_list('id', flat=True)

    signedRoles=list(profile.roles.all())
    roles_list = list(event.roles.all())

    # check if user is owner or invitee
    if (
            user_profile_id != owner_profile_id
            and user_profile_id not in invitee_profile_ids
            and user_profile_id not in attendee_profile_ids
    ):
        return HttpResponseRedirect("/account/dashboard")

    if owner_profile_id == user_profile_id:
        return HttpResponseRedirect("/planner/event_owned/{:d}/".format(event.id))

    return HttpResponse(
        render(request, 'planner/event_home.html', {'event': event, 'invitees': invitees, 'attendees': attendees, "roles_list": roles_list, "signedRoles": signedRoles})
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


#class RoleDetails(forms.Form):
    #role_name = forms.CharField(max_length=30)

class RoleForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=100)  
    amount = forms.IntegerField()


def addRoles(request, event_id):

    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")
    event = Event.objects.all().filter(id__exact=event_id).get()
    
    match request.method:
        case "GET":
            template=loader.get_template("planner/addRoles.html")
            addRoles_form=RoleForm()
            return HttpResponse(template.render(
                {
                    "addRoles_form": addRoles_form,
                },
                request
            ))
        case "POST":
            addRoles_form=RoleForm(request.POST)
            if addRoles_form.is_valid():
                role = Role(
                    name=addRoles_form.cleaned_data["name"],
                    description=addRoles_form.cleaned_data["description"],
                    amount = addRoles_form.cleaned_data["amount"],
                    event = event
            )
         
            role.save()
            #addRoles_form=RoleForm()
            return HttpResponseRedirect("/planner/event_owned/{:d}/".format(event_id))


def handle_event(request, event_id):
    # if user is not signed in, redirect to login
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

    event = Event.objects.all().filter(id__exact=event_id).get()

    if request.method == 'POST':
        action = request.POST.get('action')
        user_profile = request.user.profile

        if action == 'accept':
            event.attendees.add(user_profile)
            event.invitees.remove(user_profile)
        elif action == 'decline':
            event.invitees.remove(user_profile)

    return HttpResponseRedirect(reverse('planner:dashboard'))

def signupRoles(request, role_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/account/login/")

   
    profile_id = request.user.profile.id
    role=Role.objects.all().filter(id__exact=role_id).get()
    profile = Profile.objects.all().filter(id=profile_id).get()
  

    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user.id
        
        if action == 'accept':
            profile.roles.add(role)

    return HttpResponse(
        render(request, 'planner/signupRoles.html')
    )



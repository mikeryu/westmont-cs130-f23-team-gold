from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import django.forms as forms


def dashboard(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    template = loader.get_template('planner/dashboard.html')
    return HttpResponse(template.render({}, request))


class EventCreationForm(forms.Form):
    event_name = forms.CharField(label="Event Name:", max_length=100)
    event_location = forms.CharField(label="Event Location:", max_length=100)


def event_creation(request):
    if request.user.is_anonymous:  # User is redirected to log in if they are not logged in
        return HttpResponseRedirect("/account/login/")

    template = loader.get_template('planner/event_creation.html')
    form = EventCreationForm()
    return HttpResponse(template.render({"form": form}, request))

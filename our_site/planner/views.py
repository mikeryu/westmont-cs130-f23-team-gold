from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def landing(request):
    template = loader.get_template('planner/landing.html')
    return HttpResponse(template.render({}, request))


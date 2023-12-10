"""
This is a separate url pattern file with just one pattern in it: an empty one.
This exists to be included in the main urls.py so that if you just go to the website with no arguments,
you end up at the login page.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.PlannerLoginView.as_view(), name="login"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("event_creation/", views.event_creation, name="event_creation")
]

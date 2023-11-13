from django.urls import path


from . import views

app_name = "planner"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("event_creation/", views.event_creation, name="event_creation"),
    path("<int:event_id>/edit_event/", views.edit_event, name="edit_event"),
    path("<int:event_id>/invitations/", views.invitations, name="invitations")
]

from django.urls import path
from . import views

app_name = "planner"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Main page where user views events

    path("event_creation/", views.event_creation, name="event_creation"),  # Place to create and edit events
    path("<int:event_id>/edit_event/", views.edit_event, name="edit_event"),

    path('event/<int:event_id>/', views.event_home, name='event_home'),  # Places to view a specific event
    path('event_owned/<int:event_id>/', views.event_home_owned, name="event_home_owned"),

    path("<int:event_id>/invitations/", views.invitations, name="invitations"),  # Changing info about an event
    path('addRoles/', views.addRoles, name="addRoles"),
    path('<int:event_id>/handle_event/', views.handle_event, name='handle_event'),
]


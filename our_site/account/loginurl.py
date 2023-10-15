from django.urls import path

from . import views

urlpatterns = [
    path("", views.PlannerLoginView.as_view(), name="login"),
]

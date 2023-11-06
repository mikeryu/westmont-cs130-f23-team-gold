from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.PlannerLoginView.as_view(), name="login"),
    path("", views.PlannerLoginView.as_view(), name="login"),
    path("newAccount/", views.newAccount, name="newAccount"),
]

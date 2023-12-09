from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("login/", views.PlannerLoginView.as_view(), name="login"),
    path("", views.PlannerLoginView.as_view(), name="login"),
    path("newAccount/", views.newAccount, name="newAccount"),
    path("logout/", views.logout_view, name="logout"),
]

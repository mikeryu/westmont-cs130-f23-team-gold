from django.shortcuts import render
import django.contrib.auth.views as auth_views


class PlannerLoginView(auth_views.LoginView):
    next_page = "/planner/dashboard/"

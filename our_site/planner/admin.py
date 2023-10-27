from django.contrib import admin
from .models import Profile
from .models import Role
from .models import Event

admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(Event)

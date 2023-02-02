from django.contrib import admin
from .models import (
   Location,
   County,
   UserProfile
)

admin.site.register(Location)
admin.site.register(County)
admin.site.register(UserProfile)



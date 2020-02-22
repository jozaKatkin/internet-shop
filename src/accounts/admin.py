from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)

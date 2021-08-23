from django.contrib import admin

# Register your models here.
from jobs_portal.profiles.models import ProfileModel


@admin.register(ProfileModel)
class AuthorAdmin(admin.ModelAdmin):
    pass

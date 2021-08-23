from django.contrib import admin

# Register your models here.
from jobs_portal.job_auth.models import AppBaseUserModel


@admin.register(AppBaseUserModel)
class AuthorAdmin(admin.ModelAdmin):
    pass

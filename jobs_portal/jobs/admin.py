from django.contrib import admin

from jobs_portal.jobs.models import JobModel


@admin.register(JobModel)
class JobAdmin(admin.ModelAdmin):
    pass

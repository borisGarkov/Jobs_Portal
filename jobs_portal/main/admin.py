from django.contrib import admin


# Register your models here.
from jobs_portal.jobs.models import Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

# Register your models here.
from jobs_portal.payments.models import Payments, UserSubscriptionPlan


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscriptionPlan)
class UserSubscriptionPlanAdmin(admin.ModelAdmin):
    pass

from django.urls import path

from jobs_portal.payments.views import PricingListView

urlpatterns = [
    path('pricing-list/', PricingListView.as_view(), name='pricing-list'),
]

from django.urls import path

from jobs_portal.payments.views import *

urlpatterns = [
    path('pricing-list/', PricingListView.as_view(), name='pricing-list'),
    path('landing-checkout/<int:pk>/', LandingCheckoutView.as_view(), name='landing-checkout'),
    path('success-checkout/', SuccessCheckoutView.as_view(), name='success-checkout'),
    path('cancel-checkout/', CancelCheckoutView.as_view(), name='cancel-checkout'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel-subscription', cancel_subscription, name='cancel-subscription'),
    path('stripe-webhook/', my_webhook_view, name='webhook')
]

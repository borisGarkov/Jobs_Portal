import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from jobs_portal.payments.models import Payments, UserSubscriptionPlan
from utils.find_stripe_info import find_stripe_customer, find_customer_subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


class LandingCheckoutView(TemplateView):
    template_name = 'payments/landing-checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['pk']
        context['product'] = Payments.objects.get(pk=product_id)
        return context


class SuccessCheckoutView(TemplateView):
    template_name = 'payments/success.html'


class CancelCheckoutView(TemplateView):
    template_name = 'payments/cancel.html'


class PricingListView(TemplateView):
    template_name = 'pricing-list.html'


def cancel_subscription(request):
    customer = find_stripe_customer(current_user_email=request.user.email)
    subscription_to_delete = find_customer_subscription(current_customer_id=customer)

    if request.method == 'GET':
        context = {
            'form': 'form',
        }
        return render(request, 'payments/cancel-subscription.html', context)
    else:
        stripe.Subscription.delete(subscription_to_delete)
        stripe.Customer.delete(customer)

        current_user = UserSubscriptionPlan.objects.get(user=request.user.id)
        current_user.subscription_plan = Payments.objects.get(pk=1)
        current_user.save()

        messages.warning(request, 'Успешно деактивирахте абонамента си!')
        return redirect(reverse('profile', kwargs={'pk': request.user.id}))


@method_decorator(login_required, name='dispatch')
class CreateCheckoutSessionView(View):
    PRODUCT_IDS = {
        1: settings.STRIPE_FREE_PLAN_ID,
        2: settings.STRIPE_STANDARD_PLAN_ID,
        3: settings.STRIPE_PREMIUM_PLAN_ID,
    }

    def post(self, request, *args, **kwargs):
        current_user_email = request.user.email
        current_customer_id = ''
        subscription_to_delete = ''
        subscription_id = self.PRODUCT_IDS[kwargs['pk']]
        product_id = kwargs['pk']

        if product_id == request.user.usersubscriptionplan.subscription_plan_id:
            messages.success(self.request,
                             'Вече имате абонамент за този план!')
            return HttpResponseRedirect(reverse('home'))

        if product_id == 1:
            messages.warning(self.request,
                             'Ако желаете да преминете към безплатния абонамент, '
                             'моля първо деактивирайте платения си план от настройките в профила си!')
            return HttpResponseRedirect(reverse('home'))

        current_customer_id = find_stripe_customer(current_user_email=current_user_email)
        subscription_to_delete = find_customer_subscription(current_customer_id=current_customer_id)

        domain = request.META['HTTP_ORIGIN']

        session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            success_url=domain + reverse('success-checkout'),
            cancel_url=domain + reverse('cancel-checkout'),
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': subscription_id,
                    'quantity': 1
                }
            ],
            metadata={
                'product_id': product_id,
                'username': request.user.username,
                'user_id': request.user.id,
                'subscription_to_delete': subscription_to_delete,
            }
        )

        return redirect(session.url, code=303)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    # if event.type == 'payment_intent.succeeded':
    if event.type == 'checkout.session.completed':

        payment_intent = event.data.object  # contains a stripe.PaymentIntent

        customer_email = payment_intent['customer_details']['email']
        product_id = payment_intent['metadata']['product_id']
        username = payment_intent['metadata']['username']
        user_id = payment_intent['metadata']['user_id']
        subscription_to_delete = payment_intent['metadata']['subscription_to_delete']

        if subscription_to_delete != '':
            stripe.Subscription.delete(subscription_to_delete)

        current_user = UserSubscriptionPlan.objects.get(user=user_id)
        current_user.subscription_plan = Payments.objects.get(pk=product_id)
        current_user.save()

        message = render_to_string('payments/payment-successful-email.html', {
            'username': username
        })

        email = EmailMessage(
            subject='Успешно Плащане!',
            body=message,
            to=[customer_email],
            bcc=['rentahandbg@gmail.com', 'boris.garkov@abv.bg'],
        )

        email.send()

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

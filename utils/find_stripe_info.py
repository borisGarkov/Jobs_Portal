import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def find_stripe_customer(current_user_email):
    current_customer_id = ''

    for customer in stripe.Customer.list().data:
        if customer['email'] == current_user_email:
            current_customer_id = customer['id']
            break

    return current_customer_id


def find_customer_subscription(current_customer_id):
    subscription_to_delete = ''

    if current_customer_id != '':
        for sub in stripe.Subscription.list().data:
            if sub['customer'] == current_customer_id:
                subscription_to_delete = sub['id']
                break

    return subscription_to_delete

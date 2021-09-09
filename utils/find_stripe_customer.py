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

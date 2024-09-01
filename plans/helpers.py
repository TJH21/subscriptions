# helpers.py

import stripe
from .models import Customer

def get_or_create_stripe_customer(user, stripe_token):
    """
    Retrieves a Stripe customer if one exists, otherwise creates a new one.
    """
    try:
        # Try to get the customer from your database
        customer = Customer.objects.get(user=user)
        # Retrieve the corresponding Stripe customer
        stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
        print(f"Retrieved existing Stripe customer: {stripe_customer.id}")
    except Customer.DoesNotExist:
        try:
            # Create a new Stripe customer if it doesn't exist in your database
            stripe_customer = stripe.Customer.create(email=user.email, source=stripe_token)
            print(f"Created new Stripe customer: {stripe_customer.id}")
            customer = Customer(user=user, stripe_customer_id=stripe_customer.id)
            customer.save()
        except Exception as e:
            print(f"Error during Stripe customer creation: {str(e)}")
            return None, None

    return customer, stripe_customer

def create_stripe_subscription(stripe_customer_id, plan_id, coupon_code=None):
    """
    Creates a Stripe subscription for the given customer, plan, and optional coupon.
    """
    try:
        subscription_data = {
            'customer': stripe_customer_id,
            'items': [{'price': plan_id}],  # Ensure 'price' is correct
        }

        if coupon_code:
            subscription_data['coupon'] = coupon_code

        # Log the subscription data being sent to Stripe
        print(f"Creating subscription with data: {subscription_data}")

        subscription = stripe.Subscription.create(**subscription_data)

    except stripe.error.StripeError as e:
        # Log the exact error from Stripe
        print(f"Stripe error: {e.user_message}")
        raise e

    return subscription



def map_plan_to_stripe_id(plan_type, billing_cycle):
    """
    Maps the given plan type and billing cycle to the corresponding Stripe plan ID.
    """
    plan_mapping = {
        'basic_monthly': 'price_1PsZNRHjvVBC2HYe5oG7oDdg',
        'basic_yearly': 'price_1PsZOsHjvVBC2HYeFX5wCYcZ',
        'premium_monthly': 'price_1PsZRZHjvVBC2HYeSZKwLsZ0',
        'premium_yearly': 'price_1PsZSIHjvVBC2HYeqwbN7oJD',
        'enterprise_monthly': 'price_1PsZVOHjvVBC2HYe5nDWd4zt',
        'enterprise_yearly': 'price_1PsZWwHjvVBC2HYey0J9hlof',
    }

    plan_key = f'{plan_type}_{billing_cycle}'
    plan_id = plan_mapping.get(plan_key, None)

    # Debug output
    print(f"Plan Type: {plan_type}, Billing Cycle: {billing_cycle}, Plan Key: {plan_key}, Plan ID: {plan_id}")

    return plan_id

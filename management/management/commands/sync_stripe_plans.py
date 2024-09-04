import stripe
from django.conf import settings
from django.core.management.base import BaseCommand
from plans.models import Plan

stripe.api_key = settings.STRIPE_SECRET_KEY

class Command(BaseCommand):
    help = 'Sync Stripe plans with the local database'

    def handle(self, *args, **options):
        stripe_plans = stripe.Price.list()

        for stripe_plan in stripe_plans['data']:
            product_id = stripe_plan['product']

            # Fetch the full product details from Stripe
            product = stripe.Product.retrieve(product_id)
            product_name = product.get('name', 'Unnamed Plan').lower()

            # Determine the plan type based on product name or other criteria
            if 'enterprise' in product_name:
                plan_type = 'enterprise'
            elif 'premium' in product_name:
                plan_type = 'premium'
            elif 'basic' in product_name:
                plan_type = 'basic'
            else:
                plan_type = 'basic'  # Default to 'basic' if no match is found

            # Update or create the plan in the local database
            plan, created = Plan.objects.update_or_create(
                stripe_plan_id=stripe_plan['id'],
                defaults={
                    'name': product.get('name', 'Unnamed Plan'),
                    'description': product.get('description', ''),
                    'price': stripe_plan['unit_amount'] / 100,  # assuming price is in cents
                    'currency': stripe_plan['currency'],  # Include the currency field
                    'billing_cycle': stripe_plan['recurring']['interval'],
                    'plan_type': plan_type,  # Set the plan_type based on the logic above
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" (ID: {plan.stripe_plan_id}) created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" (ID: {plan.stripe_plan_id}) updated successfully.'))

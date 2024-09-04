import csv
from django.core.management.base import BaseCommand
from plans.models import Plan

class Command(BaseCommand):
    help = 'Load Stripe plans from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='C:/Users/Dell/OneDrive/Desktop/DATALOADS/DATALOADS/stripe_plans_001.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plan, created = Plan.objects.update_or_create(
                    stripe_plan_id=row['Price ID'],
                    defaults={
                        'name': row['Product Name'],
                        'description': row.get('Description', ''),
                        'price': int(row['Amount']),
                        'currency': row['Currency'],
                        'billing_cycle': row['Interval'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" created successfully.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" updated successfully.'))

        self.stdout.write(self.style.SUCCESS('CSV loading completed.'))

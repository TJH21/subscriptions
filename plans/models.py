from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Plan(models.Model):
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise')
    ]

    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='usd')  # Adjust max_length and default value as needed
    is_premium = models.BooleanField(default=False)  # Updated field name
    plan_type = models.CharField(max_length=50, choices=PLAN_TYPES)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLES)
    is_premium = models.BooleanField(default=False)
    stripe_plan_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.plan_type} - {self.billing_cycle})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    membership = models.BooleanField(default=False)
    cancel_at_period_end = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

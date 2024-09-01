from django.db import models
from django.contrib.auth.models import User

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

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_premium = models.BooleanField(default=False)  # Updated field name
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, default='basic')
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLES, default='monthly')
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

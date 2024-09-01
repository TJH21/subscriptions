from django import forms
from .models import Plan  # Reference the Plan model from subscriptions

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'price', 'plan_type', 'billing_cycle']
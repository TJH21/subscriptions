from django import forms
from .models import Plan  # Reference the Plan model from subscriptions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'price', 'plan_type', 'billing_cycle']


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

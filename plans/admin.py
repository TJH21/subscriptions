from django.contrib import admin
from .models import Plan
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

admin.site.register(Token, TokenAdmin)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'billing_cycle', 'price')  # Customize the display in the admin interface

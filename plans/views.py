from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Plan, Customer
from .forms import CustomSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import stripe
from .helpers import get_or_create_stripe_customer, create_stripe_subscription, map_plan_to_stripe_id


stripe.api_key = 'sk_test_51PsZIxHjvVBC2HYeiAfWxe4HlfiTr25C1FywMCsX2rfgbAMnT7oDp3PN9Sh8RWTf3ksf17W97t1Tu8K0YoKPuEoA00tsX4WNSJ'


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
            customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('Completed')


def home(request):
    plans = Plan.objects.all()
    return render(request, "plans/home.html", {"plans": plans})

def plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if plan.is_premium:
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                    return render(request, 'plans/plan.html', {'plan': plan})
            except Customer.DoesNotExist:
                return redirect('join')
        return redirect('join')
    else:
        return render(request, 'plans/plan.html', {'plan': plan})

def join(request):
    plans = Plan.objects.all()
    return render(request, 'plans/join.html')


# In subscriptions/views.py
@login_required
def checkout(request):
    # Check if the user already has an active subscription
    try:
        if request.user.customer.membership:
            return redirect('home')  # or render a page informing them that they are already subscribed
    except Customer.DoesNotExist:
        pass  # Continue if the customer doesn't exist

    coupons = {'halloween': 15, 'welcome': 10}

    if request.method == 'POST':
        try:
            # Get or create the Stripe customer
            customer, stripe_customer = get_or_create_stripe_customer(request.user, request.POST.get('stripeToken'))
        except Exception as e:
            print(f"Error during customer retrieval or creation: {e}")
            return HttpResponse("Error creating or retrieving customer.", status=400)

        # Map plan type and billing cycle to Stripe plan ID
        plan_type = request.POST.get('plan_type')
        billing_cycle = request.POST.get('billing_cycle')
        plan_id = map_plan_to_stripe_id(plan_type, billing_cycle)

        # Debugging: Print the plan ID
        print(f"Plan ID: {plan_id}")

        # Ensure the plan_id is not None
        if plan_id is None:
            return HttpResponse("Invalid plan selected.", status=400)

        # Create the Stripe subscription using the helper function
        try:
            subscription = create_stripe_subscription(
                stripe_customer_id=stripe_customer.id,
                plan_id=plan_id,
                coupon_code=request.POST.get('coupon', '').lower() if request.POST.get('coupon', '').lower() in coupons else None
            )
        except Exception as e:
            print(f"Error during subscription creation: {e}")
            return HttpResponse(f"Error creating subscription: {str(e)}", status=400)

        # Update the customer record in your database
        customer.stripe_subscription_id = subscription.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.save()

        return redirect('home')

    else:
        # Handle GET request, such as showing the checkout page with plan and pricing details
        plan_type = request.GET.get('plan_type', 'basic')
        billing_cycle = request.GET.get('billing_cycle', 'monthly')

        # Use the helper function to get the correct plan ID and pricing
        plan_id = map_plan_to_stripe_id(plan_type, billing_cycle)

        price_mapping = {
            ('basic', 'monthly'): 1000,
            ('basic', 'yearly'): 10000,
            ('premium', 'monthly'): 2500,
            ('premium', 'yearly'): 22000,
            ('enterprise', 'monthly'): 3500,
            ('enterprise', 'yearly'): 32000,
        }

        price = price_mapping.get((plan_type, billing_cycle), 1000)
        og_pound = price // 100
        coupon_pound = 0
        final_pound = og_pound

        if request.GET.get('coupon') and request.GET.get('coupon').lower() in coupons:
            coupon = request.GET['coupon'].lower()
            percentage = coupons[coupon]
            coupon_price = int((percentage / 100) * price)
            price = price - coupon_price
            coupon_pound = coupon_price // 100
            final_pound = price // 100

        return render(request, 'plans/checkout.html', {
            'plan_type': plan_type,
            'billing_cycle': billing_cycle,
            'coupon': request.GET.get('coupon', 'none'),
            'price': price,
            'og_pound': og_pound,
            'coupon_pound': coupon_pound,
            'final_pound': final_pound
        })


@login_required
def profile(request):
    customer = request.user.customer
    return render(request, 'profile.html', {'customer': customer})



def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        subscription.save()
        request.user.customer.cancel_at_period_end = True
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'registration/setting.html', {
        'membership': membership,
        'cancel_at_period_end': cancel_at_period_end
    })

class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

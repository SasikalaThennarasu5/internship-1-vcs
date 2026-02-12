from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Subscription
import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

# STEP 1: Plan selection
@login_required
def plan_select(request):
    subscription, created = Subscription.objects.get_or_create(
        user=request.user
    )

    return render(request, "subscriptions/plan_select.html", {
        "subscription": subscription
    })


# STEP 2: Free plan (no payment)
@login_required
def activate_free(request):
    subscription, created = Subscription.objects.get_or_create(
        user=request.user
    )

    subscription.plan = "FREE"
    subscription.is_active = True
    subscription.start_date = timezone.now()
    subscription.end_date = None
    subscription.save()

    messages.success(request, "Free plan activated 🎉")
    return redirect("subscriptions:success")


# STEP 3: Payment page 
@login_required
def payment(request, plan):
    plans = {
        "PRO": {"name": "Pro", "amount": 999, "days": 30},
        "PRO_PLUS": {"name": "Pro Plus", "amount": 29999, "days": 365},
    }

    plan_data = plans.get(plan)
    if not plan_data:
        return redirect("subscriptions:plan_select")

    # Convert to paise
    amount_in_paise = plan_data["amount"] * 100

    # Create Razorpay client
    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    # Create order
    order = client.order.create({
    "amount": amount_in_paise,
    "currency": "INR",
    "payment_capture": 1,
    "notes": {
        "plan": plan
    }
})

    return render(request, "subscriptions/payment.html", {
        "plan": plan,
        "plan_name": plan_data["name"],
        "amount": plan_data["amount"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"],
    })

# STEP 4: Payment success (ACTIVATE subscription)
@login_required
def payment_success(request, plan):

    if request.method != "POST":
        return redirect("subscriptions:plan_select")

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

         # ✅ STEP 2: Fetch order from Razorpay
        order_data = client.order.fetch(order_id)

        # ✅ STEP 3: Get plan from order notes (NOT from URL)
        plan = order_data["notes"]["plan"]

    except Exception as e:
        messages.error(request, "Payment verification failed ❌")
        return redirect("subscriptions:plan_select")

    # ✅ STEP 4: Activate subscription safely
    subscription, created = Subscription.objects.get_or_create(
        user=request.user
    )

    subscription.plan = plan
    subscription.is_active = True
    subscription.start_date = timezone.now()

    if plan == "PRO":
        subscription.end_date = timezone.now() + timedelta(days=30)
    elif plan == "PRO_PLUS":
        subscription.end_date = timezone.now() + timedelta(days=365)

    subscription.save()

    messages.success(request, "Payment successful 🎉 Plan activated")
    return redirect("subscriptions:success")


# STEP 5: Success page
@login_required
def success(request):
    subscription = Subscription.objects.get(user=request.user)
    return render(request, "subscriptions/success.html", {
        "subscription": subscription
    })

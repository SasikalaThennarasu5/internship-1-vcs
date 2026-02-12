from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Consultant, ConsultantSession
from subscriptions.models import Subscription
from notifications.models import Notification


@login_required
def schedule_session(request):
    subscription = Subscription.objects.get(user=request.user)

    if subscription.plan == "FREE":
        messages.error(request, "Upgrade to access consultants")
        return redirect("subscriptions:plan_select")

    if request.method == "POST":
        consultant_id = request.POST.get("consultant")
        scheduled_at = request.POST.get("scheduled_at")

        sla = 4 if subscription.plan == "PRO" else 2

        ConsultantSession.objects.create(
            user=request.user,
            consultant_id=consultant_id,
            plan=subscription.plan,
            scheduled_at=scheduled_at,
            sla_hours=sla
        )

        Notification.objects.create(
            user=request.user,
            title="Consultant Session Scheduled",
            message="Your consultant session has been booked.",
            channel="SYSTEM"
        )

        messages.success(request, "Session scheduled successfully")
        return redirect("consultants:my_sessions")

    consultants = Consultant.objects.filter(is_active=True)
    return render(request, "consultants/schedule.html", {
        "consultants": consultants
    })

@login_required
def my_calendar(request):
    sessions = ConsultantSession.objects.filter(
        user=request.user
    ).order_by("scheduled_at")

    return render(request, "consultants/calendar.html", {
        "sessions": sessions
    })

@login_required
def my_sessions(request):
    sessions = ConsultantSession.objects.filter(user=request.user)

    return render(request, "consultants/my_sessions.html", {
        "sessions": sessions
    })
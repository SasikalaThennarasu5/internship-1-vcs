from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .models import MockInterview
from subscriptions.models import Subscription
from notifications.utils import create_notification


# ---------------------------
# BOOK MOCK INTERVIEW (PRO PLUS)
# ---------------------------
@login_required
def book_mock_interview(request):

    subscription = Subscription.objects.filter(user=request.user).first()

    if not subscription or subscription.plan != "PRO_PLUS":
        messages.error(request, "Mock interviews are available only for Pro Plus users.")
        return redirect("/subscriptions/plan_select/")

    if request.method == "POST":

        interview_type = request.POST.get("interview_type")
        scheduled_at = request.POST.get("scheduled_at")

        # 🔥 Get assigned consultant from profile
        profile = request.user.profile
        consultant = profile.assigned_consultant

        if not consultant:
            messages.error(request, "No consultant assigned. Please contact admin.")
            return redirect("dashboard:user")

        MockInterview.objects.create(
            user=request.user,
            consultant=consultant,
            interview_type=interview_type,
            scheduled_at=scheduled_at,
            status="SCHEDULED"
        )

        messages.success(request, "Mock interview booked successfully.")
        return redirect("mock_interviews:my_interviews")

    return render(request, "mock_interviews/book.html")




# ---------------------------
# USER VIEW – MY INTERVIEWS
# ---------------------------
@login_required
def my_mock_interviews(request):
    interviews = MockInterview.objects.filter(user=request.user)
    return render(request, "mock_interviews/my_interviews.html", {
        "interviews": interviews
    })


# ---------------------------
# CONSULTANT – MARK COMPLETED
# ---------------------------
@login_required
def mark_interview_completed(request, interview_id):
    interview = get_object_or_404(MockInterview, id=interview_id,  consultant=request.user)

    if request.method == "POST":
     interview.status = "COMPLETED"
     interview.completed_at = timezone.now()
     interview.save()
    

    create_notification(
        user=interview.user,
        title="Mock Interview Completed",
        message="Your mock interview has been marked as completed."
    )

    messages.success(request, "Interview marked as completed.")
    return redirect("mock_interviews:upload_feedback", interview_id=interview.id)


# ---------------------------
# CONSULTANT – UPLOAD FEEDBACK
# ---------------------------
@login_required
def upload_feedback(request, interview_id):
    interview = get_object_or_404(MockInterview, id=interview_id)

    if request.method == "POST":
        interview.feedback = request.POST.get("feedback")
        interview.rating = request.POST.get("rating")
        interview.status = "COMPLETED"
        interview.save()

        create_notification(
            user=interview.user,
            title="Mock Interview Feedback Ready",
            message="Your mock interview feedback has been uploaded."
        )

        messages.success(request, "Feedback uploaded successfully.")
        return redirect("mock_interviews:consultant_dashboard")

    return render(
        request,
        "mock_interviews/upload_feedback.html",
        {"interview": interview}
    )

@login_required
def consultant_dashboard(request):

    if request.user.profile.role != "CONSULTANT":
        return HttpResponseForbidden("Not allowed")

    interviews = MockInterview.objects.filter(
        consultant=request.user
    )

    total = interviews.count()
    scheduled = interviews.filter(status="SCHEDULED").count()
    completed = interviews.filter(status="COMPLETED").count()
    cancelled = interviews.filter(status="CANCELLED").count()

    # 📅 Upcoming Today
    today = timezone.now().date()
    upcoming_today = interviews.filter(
        scheduled_at__date=today,
        status="SCHEDULED"
    )

    # 🚨 SLA Breach (24 hours rule example)
    breached = interviews.filter(
        status="SCHEDULED",
        scheduled_at__lt=timezone.now() - timedelta(hours=24)
    )

    return render(
        request,
        "mock_interviews/consultant_dashboard.html",
        {
            "interviews": interviews,
            "total": total,
            "scheduled": scheduled,
            "completed": completed,
            "cancelled": cancelled,
            "upcoming_today": upcoming_today,
            "breached": breached,
        }
    )

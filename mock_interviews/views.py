from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .models import MockInterview
from subscriptions.models import Subscription
from notifications.utils import create_notification
from django.contrib.auth.models import User


# ---------------------------
# BOOK MOCK INTERVIEW (PRO PLUS)
# ---------------------------
@login_required
def book_mock_interview(request):

    subscription = Subscription.objects.filter(user=request.user).first()

    if not subscription or subscription.plan != "PRO_PLUS":
        messages.error(request, "Mock interviews are available only for Pro Plus users.")
        return redirect("subscriptions:plan_select")

    if request.method == "POST":

        interview_type = request.POST.get("interview_type")
        scheduled_at = request.POST.get("scheduled_at")

        MockInterview.objects.create(
            user=request.user,
            interview_type=interview_type,
            scheduled_at=scheduled_at,
            status="PENDING"
        )

        messages.success(request, "Booking request sent. Admin will assign consultant soon.")
        return redirect("dashboard:user")

    # ✅ THIS MUST BE OUTSIDE POST BLOCK
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
from django.utils import timezone

@login_required
def mark_interview_completed(request, interview_id):
    interview = get_object_or_404(
        MockInterview,
        id=interview_id,
        consultant=request.user
    )

    if request.method == "POST":
        interview.status = "COMPLETED"
        interview.completed_at = timezone.now()
        interview.save()

        # Notify candidate
        create_notification(
            user=interview.user,
            title="Mock Interview Completed",
            message="Your mock interview has been marked as completed."
        )

        messages.success(request, "Interview marked as completed.")
        return redirect(
            "mock_interviews:upload_feedback",
            interview_id=interview.id
        )

    return redirect("mock_interviews:consultant_dashboard")



# ---------------------------
# CONSULTANT – UPLOAD FEEDBACK
# ---------------------------
@login_required
def upload_feedback(request, interview_id):
    interview = get_object_or_404(
        MockInterview,
        id=interview_id,
        consultant=request.user  # 🔐 restrict to assigned consultant
    )

    # Prevent duplicate feedback
    if interview.status == "COMPLETED" and interview.feedback:
        messages.warning(request, "Feedback already uploaded.")
        return redirect("mock_interviews:consultant_dashboard")

    if request.method == "POST":
        feedback = request.POST.get("feedback")
        rating = request.POST.get("rating")

        # Basic validation
        if not feedback:
            messages.error(request, "Feedback cannot be empty.")
            return redirect("mock_interviews:upload_feedback", interview_id=interview.id)

        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect("mock_interviews:upload_feedback", interview_id=interview.id)

        interview.feedback = feedback
        interview.rating = rating
        interview.status = "COMPLETED"
        interview.completed_at = timezone.now()
        interview.save()

        # Notify candidate
        create_notification(
            user=interview.user,
            title="Mock Interview Feedback Ready",
            message="Your mock interview feedback has been uploaded."
        )

        messages.success(request, "Feedback uploaded successfully.")
        return redirect("mock_interviews:consultant_dashboard")

    return render(request, "mock_interviews/upload_feedback.html", {
        "interview": interview
    })


@login_required
def consultant_dashboard(request):

    if request.user.profile.role != "CONSULTANT":
        return HttpResponseForbidden("Not allowed")

    interviews = MockInterview.objects.filter(
        consultant=request.user
    )

    total = interviews.count()
    assigned = interviews.filter(status="ASSIGNED").count()
    scheduled = interviews.filter(status="SCHEDULED").count()
    completed = interviews.filter(status="COMPLETED").count()
    cancelled = interviews.filter(status="CANCELLED").count()

    today = timezone.now().date()

    upcoming_today = interviews.filter(
        scheduled_at__date=today,
        status="SCHEDULED"
    )

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
            "assigned": assigned,
            "scheduled": scheduled,
            "completed": completed,
            "cancelled": cancelled,
            "upcoming_today": upcoming_today,
            "breached": breached,
        }
    )


@login_required
def assign_mock_interview(request, interview_id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    interview = get_object_or_404(MockInterview, id=interview_id)

    if request.method == "POST":
        consultant_id = request.POST.get("consultant")
        meeting_link = request.POST.get("meeting_link")

        interview.consultant_id = consultant_id
        interview.meeting_link = meeting_link
        interview.status = "SCHEDULED"
        interview.save()

        messages.success(request, "Interview scheduled successfully.")
        return redirect("dashboard:admin")

    consultants = User.objects.filter(profile__role="CONSULTANT")

    return render(request, "mock_interviews/assign.html", {
        "interview": interview,
        "consultants": consultants
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job, JobApplication
from profiles.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.contrib.auth.models import User
from training.models import CourseEnrollment
from django.core.mail import send_mail
from django.conf import settings
from subscriptions.models import Subscription
from consultants.models import ConsultantSession
from mock_interviews.models import MockInterview
from resume.models import ResumeReview

from django.http import HttpResponseForbidden
from notifications.utils import create_notification


@login_required
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard:user')

    jobs = Job.objects.all()
    applications = JobApplication.objects.select_related('job', 'user')
    pending_interviews = MockInterview.objects.filter(status="PENDING")
    pending_sessions = ConsultantSession.objects.filter(status="PENDING")

    context = {
        "jobs": jobs,
        "applications": applications,
        "total_jobs": jobs.count(),
        "total_applications": applications.count(),
        "pending_interviews": pending_interviews,
        "pending_sessions": pending_sessions,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def user_dashboard(request):
    # ✅ SUBSCRIPTION CHECK (ADDED)
    if not Subscription.objects.filter(user=request.user).exists():
        return redirect("/subscriptions/plans/")
    
    subscription = Subscription.objects.get(user=request.user)

    profile = Profile.objects.filter(user=request.user).first()
    applications = JobApplication.objects.filter(user=request.user)

    certificates = CourseEnrollment.objects.filter(
        user=request.user,
        completed=True
    ).select_related("course")

    consultant_sessions = ConsultantSession.objects.filter(user=request.user)
    mock_interviews = MockInterview.objects.filter(user=request.user)
    resume_reviews = ResumeReview.objects.filter(resume__user=request.user)

    completion = profile.completion_percentage if profile else 0

    return render(request, "dashboard/user_dashboard.html", {
        "profile": profile,
        "completion": completion,
        "applications": applications,
        "certificates": certificates,
        "subscription": subscription,
        "consultant_sessions": consultant_sessions,
        "mock_interviews": mock_interviews,
        "resume_reviews": resume_reviews,
    })


    

@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(JobApplication, id=app_id)

    application.status = status
    application.save()

    # 🔔 EMAIL WHEN SHORTLISTED
    if status == "shortlisted":
        subject = "🎉 Interview Shortlisted – Vetri Consultancy Services"

        message = f"""
Dear {application.user.username},

Congratulations! 🎉

You have been shortlisted for an interview.

Job Details:
- Job Title: {application.job.title}
- Company: {application.job.company}

Our HR team will contact you shortly with interview details.

Best regards,
Vetri Consultancy Services
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.user.email],
            fail_silently=False,
        )

        messages.success(request, "Candidate shortlisted and email sent 📧")

    elif status == "rejected":
        messages.warning(request, "Application rejected")

    return redirect("dashboard:admin_candidates")


def admin_candidates(request):
    if not request.user.is_staff:
        return redirect("/")

    profiles = Profile.objects.select_related("user")

    return render(request, "dashboard/admin_candidates.html", {
        "profiles": profiles
    })

@login_required
def admin_candidate_detail(request, user_id):
    if not request.user.is_staff:
        return redirect("/")

    profile = get_object_or_404(Profile, user__id=user_id)

    return render(request, "dashboard/admin_candidate_detail.html", {
        "profile": profile
    })

@login_required
def dashboard_home(request):
    if request.user.is_staff:
        return redirect('dashboard:admin')
    return redirect('dashboard:user')





@user_passes_test(lambda u: u.is_superuser)
def admin_analytics(request):

    total_jobs = Job.objects.count()
    total_users = User.objects.count()
    total_applications = JobApplication.objects.count()

    status_stats = JobApplication.objects.values("status").annotate(
        count=Count("id")
    )

    popular_jobs = Job.objects.annotate(
        app_count=Count("jobapplication")
    ).order_by("-app_count")[:5]

    context = {
        "total_jobs": total_jobs,
        "total_users": total_users,
        "total_applications": total_applications,
        "status_stats": status_stats,
        "popular_jobs": popular_jobs,
    }

    return render(request, "dashboard/admin_analytics.html", context)

@login_required
def assign_consultant_session(request, session_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    session = get_object_or_404(ConsultantSession, id=session_id)

    if request.method == "POST":
        consultant_id = request.POST.get("consultant")
        meeting_link = request.POST.get("meeting_link")

        session.consultant_id = consultant_id
        session.meeting_link = meeting_link
        session.status = "ASSIGNED"
        session.save()

        create_notification(
            user=session.user,
            title="Consultant Session Assigned",
            message=f"Your session has been assigned. Join here: {meeting_link}"
        )

        messages.success(request, "Session assigned successfully.")
        return redirect("dashboard:admin")




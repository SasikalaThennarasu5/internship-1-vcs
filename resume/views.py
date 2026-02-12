from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Resume, ResumeReview
from subscriptions.models import Subscription

@login_required
def upload_resume(request):
    subscription = Subscription.objects.get(user=request.user)

    if subscription.plan == "FREE":
        messages.error(request, "Upgrade to optimize resume")
        return redirect("subscriptions:plan_select")

    if request.method == "POST":
        resume = Resume.objects.create(
            user=request.user,
            file=request.FILES["resume"]
        )

        ResumeReview.objects.create(
            resume=resume,
            plan=subscription.plan,
            suggestions="Pending review",
            score=0
        )

        messages.success(request, "Resume uploaded for review")
        return redirect("dashboard:user")

    return render(request, "resume/upload.html")

@login_required
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)

    return render(request, "resume/my_resumes.html", {
        "resumes": resumes
    })

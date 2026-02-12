from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import CourseEnrollment
from subscriptions.models import Subscription
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from django.utils.timezone import localtime
from .models import Course




@login_required
def download_certificate(request, enrollment_id):
    enrollment = get_object_or_404(
        CourseEnrollment,
        id=enrollment_id,
        user=request.user,
        completed=True
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="certificate_{enrollment.course.title}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # 🔹 TITLE
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 150, "Certificate of Completion")

    # 🔹 BODY
    c.setFont("Helvetica", 16)
    c.drawCentredString(
        width / 2,
        height - 230,
        "This is to certify that"
    )

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(
        width / 2,
        height - 270,
        enrollment.user.username
    )

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        width / 2,
        height - 320,
        "has successfully completed the course"
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        width / 2,
        height - 360,
        enrollment.course.title
    )

    # 🔹 DATE
    completed_date = localtime(enrollment.completed_at).strftime("%d %B %Y")
    c.setFont("Helvetica", 14)
    c.drawCentredString(
        width / 2,
        height - 420,
        f"Completed on {completed_date}"
    )

    # 🔹 FOOTER
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(
        width / 2,
        100,
        "Vetri Jobs Training Platform"
    )

    c.showPage()
    c.save()

    enrollment.certificate_generated = True
    enrollment.save()

    return response

@login_required
def training_home(request):
    subscription = Subscription.objects.get(user=request.user)

    courses = Course.objects.all()
    return render(
        request,
        "training/courses.html",
        {"courses": courses}
    )

    if subscription.plan == "FREE":
        messages.error(
            request,
            "Upgrade to access training programs 🎓"
        )
        return redirect("subscriptions:plan_select")

    return render(request, "training/courses.html")

@login_required
def complete_course(request, enrollment_id):
    enrollment = get_object_or_404(
        CourseEnrollment,
        id=enrollment_id,
        user=request.user
    )

    enrollment.completed = True
    enrollment.completed_at = timezone.now()
    enrollment.save()

    messages.success(
        request,
        "Course completed successfully 🎉 Certificate unlocked!"
    )

    return redirect("training:my_courses")

@login_required
def my_courses(request):
    enrollments = CourseEnrollment.objects.filter(
        user=request.user
    )

    return render(
        request,
        "training/my_courses.html",
        {
            "enrollments": enrollments
        }
    )

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    if created:
        messages.success(
            request,
            f"Enrolled in {course.title} successfully 🎉"
        )
    else:
        messages.info(
            request,
            "You are already enrolled in this course"
        )

    return redirect("training:my_courses")
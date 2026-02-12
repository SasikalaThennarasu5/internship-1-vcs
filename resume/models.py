from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    optimized_file = models.FileField(
        upload_to="optimized_resumes/",
        null=True,
        blank=True
    )

    

    def __str__(self):
        return f"Resume - {self.user}"

class ResumeReview(models.Model):
    PLAN_CHOICES = (
        ("PRO", "Pro"),
        ("PRO_PLUS", "Pro Plus"),
    )

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)

    suggestions = models.TextField()
    score = models.IntegerField(default=0)

    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review - {self.resume.user}"

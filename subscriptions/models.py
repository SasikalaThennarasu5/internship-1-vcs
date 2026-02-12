from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Subscription(models.Model):

    PLAN_CHOICES = (
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("PRO_PLUS", "Pro Plus"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="FREE"
    )

    is_active = models.BooleanField(default=True)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    payment_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

     # monthly usage counters
    consultant_sessions_used = models.PositiveIntegerField(default=0)
    mock_interviews_used = models.PositiveIntegerField(default=0)
    resume_reviews_used = models.PositiveIntegerField(default=0)

    

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

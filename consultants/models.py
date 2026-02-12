from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Consultant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    expertise = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ConsultantSession(models.Model):
    PLAN_CHOICES = (
        ("PRO", "Pro"),
        ("PRO_PLUS", "Pro Plus"),
    )

    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consultant = models.ForeignKey(
        Consultant,
        on_delete=models.SET_NULL,
        null=True
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="FREE"   # ✅ IMPORTANT
    )
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)

    sla_hours = models.IntegerField(default=4)  # PRO=4, PRO_PLUS=2
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.scheduled_at}"

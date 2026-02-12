from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class MockInterview(models.Model):

    INTERVIEW_TYPE_CHOICES = [
        ('TECH', 'Technical'),
        ('BEHAV', 'Behavioral'),
        ('CASE', 'Case Study'),
    ]

    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consultant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mock_interviews_taken",
        limit_choices_to={'userprofile__role': 'CONSULTANT'}
    )

    interview_type = models.CharField(
        max_length=10,
        choices=INTERVIEW_TYPE_CHOICES
    )

    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )

    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_interview_type_display()}"
    
    @property
    def sla_deadline(self):
        return self.completed_at + timedelta(hours=24)

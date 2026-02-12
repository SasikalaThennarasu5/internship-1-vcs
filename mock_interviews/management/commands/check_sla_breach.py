from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from mock_interviews.models import MockInterview
from notifications.utils import create_notification


class Command(BaseCommand):
    help = "Check SLA breaches for mock interview feedback"

    def handle(self, *args, **kwargs):
        overdue = MockInterview.objects.filter(
            status="COMPLETED",
            feedback="",
            completed_at__lt=timezone.now() - timedelta(hours=24)
        )

        for interview in overdue:
            create_notification(
                user=interview.user,
                title="SLA Breach Alert",
                message="Your mock interview feedback is delayed beyond SLA."
            )

        self.stdout.write(
            self.style.SUCCESS(f"{overdue.count()} SLA breaches checked.")
        )

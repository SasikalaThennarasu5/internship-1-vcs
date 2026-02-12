from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from consultants.models import ConsultantSession
from notifications.models import Notification

class Command(BaseCommand):
    help = "Send consultant session reminders"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        upcoming_sessions = ConsultantSession.objects.filter(
            status="SCHEDULED",
            scheduled_at__gte=now,
            scheduled_at__lte=now + timedelta(hours=24)
        )

        for session in upcoming_sessions:
            Notification.objects.get_or_create(
                user=session.user,
                title="Consultant Session Reminder",
                message=f"Your session with {session.consultant} is scheduled at {session.scheduled_at}.",
                channel="SYSTEM"
            )

        self.stdout.write("Session reminders sent")

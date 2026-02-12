from django.db import models
from consultants.models import ConsultantSession


class SessionNote(models.Model):
    session = models.OneToOneField(
        ConsultantSession,
        on_delete=models.CASCADE
    )

    notes = models.TextField()
    feedback = models.TextField(null=True,
        blank=True)
    rating = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for session {self.session.id}"

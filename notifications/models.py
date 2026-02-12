from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    CHANNEL_CHOICES = (
        ("EMAIL", "Email"),
        ("WHATSAPP", "WhatsApp"),
        ("SYSTEM", "System"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()

    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="SYSTEM" )
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

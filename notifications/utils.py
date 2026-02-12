from .models import Notification   # 👈 ADD THIS

def create_notification(user, title, message):
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )

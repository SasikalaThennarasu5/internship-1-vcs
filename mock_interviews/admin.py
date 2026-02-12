from django.contrib import admin
from .models import MockInterview


@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "consultant",
        "interview_type",
        "scheduled_at",
        "status",          # ✅ FIX
    )

    list_filter = (
        "interview_type",
        "status",          # ✅ FIX
    )

    search_fields = (
        "user__username",
        "consultant__username",
    )

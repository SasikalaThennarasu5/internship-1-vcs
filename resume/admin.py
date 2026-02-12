from django.contrib import admin
from .models import Resume, ResumeReview


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "uploaded_at")
    search_fields = ("user__username",)


@admin.register(ResumeReview)
class ResumeReviewAdmin(admin.ModelAdmin):
    list_display = ("resume", "plan", "score", "reviewed_at")
    list_filter = ("plan",)

from django.contrib import admin
from .models import SessionNote


@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = ("session", "rating", "created_at")
    search_fields = ("session__user__username",)

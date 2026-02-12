from django.contrib import admin
from .models import Consultant, ConsultantSession


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "expertise", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "expertise")


@admin.register(ConsultantSession)
class ConsultantSessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "consultant",
        "plan",
        "scheduled_at",
        "status",
        "sla_hours",
    )
    list_filter = ("plan", "status")
    search_fields = ("user__username", "consultant__name")
    ordering = ("-scheduled_at",)

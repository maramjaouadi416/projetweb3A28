from django.contrib import admin
from .models import Appointment


@admin.action(description="make them confirmed")
def confirmed_appointment(model,req,queryset):
    queryset.update(status="CONFIRMED")


# Register your models here.
@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    actions=[confirmed_appointment]
    list_display = ("reason", "status", "duration_minutes", "appointment_date")
    list_filter = ("status", "appointment_date")
    list_editable = ("status",)
    list_per_page = 2
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Description", {
            "fields": ("reason", "status", "prescription")
        }),
        ("Date + Duration", {
            "fields": ("appointment_date", "duration_minutes")
        }),
        ("Patients/Doctors", {
            "fields": ("doctor", "patient")
        }),
        ("Planification", {
            "fields": ("created_at", "updated_at")
        }),
    )
    readonly_fields = ("created_at", "updated_at")
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accountapp.models import Doctor, Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    reason = models.TextField()
    prescription = models.FileField(blank=True, upload_to='prescription/')
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.appointment_date is None:
            return

        modified_date = self._state.adding or not Appointment.objects.filter(
            pk=self.pk,
            appointment_date=self.appointment_date
        ).exists()

        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError(
                {"appointment_date": "la date doit être dans le futur"}
            )


    class Meta:
        ordering = ["-appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name="unicite-doctor-date",
                violation_error_message="ce docteur possède un rdv avec cette date"
            )
        ]
    def _str_(self):
        return f"le rdv est pour la raison {self.reason}"
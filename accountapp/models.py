from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


number_validator = RegexValidator(
    regex=r'^\d{8}$',
    message='this number must contain 8 digits'
)


def validate_birth_date(v):
    if v >= timezone.localdate():
        raise ValidationError("la date de naissance n'est pas valide")


class User(AbstractUser):
    pass


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
def _str_(self):
    return self.name

class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)]
    )
    phone = models.CharField(max_length=8, validators=[number_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialities = models.ManyToManyField(Specialty, related_name="doctors")

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[number_validator])
    phone = models.CharField(max_length=8, validators=[number_validator])
    birth_date = models.DateField(validators=[validate_birth_date])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
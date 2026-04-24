from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Doctor(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )
    specialization = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='doctors/', blank=True, null=True)
    availability = models.JSONField(default=dict, blank=True)

    def __str__(self):
        # Display nicely as Dr Name
        return f"Dr {self.profile.user.username.title()}"


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.profile.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        patient = self.patient.profile.user.username if self.patient and self.patient.profile and self.patient.profile.user else "Unknown Patient"
        doctor = self.doctor.profile.user.username if self.doctor and self.doctor.profile and self.doctor.profile.user else "Unknown Doctor"
        return f"{patient} with {doctor} on {self.date}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
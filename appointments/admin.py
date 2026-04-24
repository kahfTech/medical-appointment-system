from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Doctor, Patient, Appointment, Booking


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_verified', 'created_at')
    list_filter = ('role',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'specialization', 'get_avatar')

    def get_username(self, obj):
        if obj.profile and obj.profile.user:
            return obj.profile.user.username
        return "No User"

    get_username.short_description = "Username"

    def get_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%"/>',
                obj.avatar.url
            )
        return "No Image"

    get_avatar.short_description = "Avatar"

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'phone')

    def get_username(self, obj):
        if obj.profile and obj.profile.user:
            return obj.profile.user.username
        return "No User"

    get_username.short_description = "Username"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'doctor')
    list_editable = ('status',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment', 'amount', 'created_at')

# Register your models here.

from django.contrib import admin
from .models import Profile, Doctor, Patient, Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'doctor')
    list_editable = ('status',)

admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment, AppointmentAdmin)

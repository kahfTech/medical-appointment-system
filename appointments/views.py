from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Patient, Doctor, Appointment, Profile, Booking


# HOME PAGE
def home(request):
    return render(request, 'appointments/home.html')


# REGISTER
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'patient')
        phone = request.POST.get('phone', '').strip()

        # VALIDATION
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please login.')
            return redirect('login')

        try:
            # AUTO GENERATE USERNAME (hidden system use only)
            username = email.split('@')[0]

            counter = 1
            base_username = username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # CREATE USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # CREATE PROFILE
            profile = Profile.objects.create(user=user, role=role)

            # ROLE MODELS
            if role == 'patient':
                Patient.objects.create(profile=profile, phone=phone)

            elif role == 'doctor':
                Doctor.objects.create(profile=profile)

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')

    return render(request, 'appointments/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # VALIDATION
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('login')

        try:
            # GET USER BY EMAIL
            user_obj = User.objects.get(email=email)
            username = user_obj.username  # Django needs username internally

            # AUTHENTICATE
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "Email not found. Please register.")
            return redirect('register')

    return render(request, 'appointments/login.html')

# MY APPOINTMENTS
@login_required(login_url='login')
def my_appointments(request):
    appointments = []

    profile = Profile.objects.filter(user=request.user).first()

    if profile:
        patient = Patient.objects.filter(profile=profile).first()

        if patient:
            appointments = Appointment.objects.filter(patient=patient)
        else:
            messages.info(request, "Patient profile not found.")
    else:
        messages.info(request, "Profile not found.")

    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments
    })


# BOOKINGS LIST
class BookingListView(ListView):
    model = Booking
    template_name = 'appointments/bookings.html'


# APPOINTMENT DETAIL
class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointments/appointment.html'
    pk_url_kwarg = 'appointment_id'


# DOCTOR APPOINTMENTS
class DoctorAppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/doctor_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        doctor_username = self.kwargs['doctor_username']
        return Appointment.objects.filter(
            doctor__profile__user__username=doctor_username
        )


# PATIENT APPOINTMENTS
class PatientAppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/patient_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        patient_username = self.kwargs['patient_username']
        return Appointment.objects.filter(
            patient__profile__user__username=patient_username
        )


# ADMIN DASHBOARD
@login_required(login_url='login')
def admin_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)

        if profile.role != 'admin':
            messages.error(request, 'Access denied.')
            return redirect('home')

        appointments = Appointment.objects.all().order_by('-created_at')
        bookings = Booking.objects.all().order_by('-created_at')

    except Profile.DoesNotExist:
        messages.error(request, 'No profile found.')
        return redirect('home')

    return render(request, 'appointments/admin_dashboard.html', {
        'appointments': appointments,
        'bookings': bookings
    })

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required(login_url='login')
def book_appointment(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        try:
            doctor_id = request.POST.get('doctor')
            date = request.POST.get('date')
            time = request.POST.get('time')
            notes = request.POST.get('notes', '')

            doctor = Doctor.objects.get(id=doctor_id)

            profile = Profile.objects.filter(user=request.user).first()

            if not profile:
                messages.error(request, "Profile not found.")
                return redirect('home')

            patient, created = Patient.objects.get_or_create(profile=profile)

            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                time=time,
                notes=notes,
                status='Pending'
            )

            messages.success(request, "Appointment booked successfully!")
            return redirect('my_appointments')

        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")

    return render(request, 'appointments/book.html', {'doctors': doctors})
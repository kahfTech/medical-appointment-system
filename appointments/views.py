# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, Doctor, Appointment, Profile

# HOME PAGE
def home(request):
    return render(request, 'appointments/home.html')

# REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        password = request.POST['password']
        phone = request.POST['phone']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile.objects.create(user=user, role='patient')
            Patient.objects.create(profile=profile, phone=phone)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    return render(request, 'appointments/register.html')

# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'appointments/login.html')

# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('home')

# BOOK APPOINTMENT
@login_required
def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        try:
            doctor_id = request.POST['doctor']
            date = request.POST['date']
            time = request.POST['time']
            doctor = Doctor.objects.get(id=doctor_id)
            profile = Profile.objects.get(user=request.user)
            patient, created = Patient.objects.get_or_create(
                profile=profile,
                defaults={'phone': ''}
            )
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                time=time,
                status='Pending'
            )
            messages.success(request, 'Appointment booked successfully!')
            return redirect('my_appointments')
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
    return render(request, 'appointments/book.html', {'doctors': doctors})

# VIEW MY APPOINTMENTS
@login_required
def my_appointments(request):
    try:
        profile = Profile.objects.get(user=request.user)
        patient = Patient.objects.get(profile=profile)
        appointments = Appointment.objects.filter(patient=patient)
    except (Profile.DoesNotExist, Patient.DoesNotExist):
        appointments = []
        messages.info(request, 'No profile/patient found. Please register properly or contact admin.')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

@login_required
def admin_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.role != 'admin':
            messages.error(request, 'Access denied. Admins only.')
            return redirect('home')
        appointments = Appointment.objects.all().order_by('-created_at')
    except Profile.DoesNotExist:
        messages.error(request, 'No profile found.')
        return redirect('home')
    return render(request, 'appointments/admin_dashboard.html', {'appointments': appointments})

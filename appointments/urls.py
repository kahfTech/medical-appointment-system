from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('bookings/', views.BookingListView.as_view(), name='bookings'),

    path(
        'appointment/<int:appointment_id>/',
        views.AppointmentDetailView.as_view(),
        name='appointment'
    ),

    path(
        'doctor/<str:doctor_username>/appointments/',
        views.DoctorAppointmentListView.as_view(),
        name='doctor_appointments'
    ),

    path(
        'patient/<str:patient_username>/appointments/',
        views.PatientAppointmentListView.as_view(),
        name='patient_appointments'
    ),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
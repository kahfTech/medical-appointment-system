from django.db import migrations

def create_doctors(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('appointments', 'Profile')
    Doctor = apps.get_model('appointments', 'Doctor')

    doctors_data = [
        {
            'username': 'dr_smith',
            'email': 'dr.smith@example.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'specialization': 'Cardiology',
            'availability': {'monday': ['09:00-12:00', '14:00-18:00'], 'wednesday': ['09:00-12:00', '14:00-18:00']},
        },
        {
            'username': 'dr_johnson',
            'email': 'dr.johnson@example.com',
            'first_name': 'Emily',
            'last_name': 'Johnson',
            'specialization': 'Neurology',
            'availability': {'tuesday': ['10:00-13:00', '15:00-19:00'], 'thursday': ['10:00-13:00', '15:00-19:00']},
        },
    ]

    for data in doctors_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='securepass123'  # Change in production
            )
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            profile = Profile.objects.create(
                user=user,
                role='doctor'
            )

            Doctor.objects.create(
                profile=profile,
                specialization=data['specialization'],
                availability=data['availability']
            )

def reverse_create_doctors(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('appointments', 'Profile')
    Doctor = apps.get_model('appointments', 'Doctor')

    for data in [
        {'username': 'dr_smith'},
        {'username': 'dr_johnson'},
    ]:
        user = User.objects.filter(username=data['username']).first()
        if user:
            profile = Profile.objects.filter(user=user, role='doctor').first()
            if profile:
                doctor = Doctor.objects.filter(profile=profile).first()
                if doctor:
                    doctor.delete()
                profile.delete()
            user.delete()

class Migration(migrations.Migration):
    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_doctors, reverse_create_doctors),
    ]

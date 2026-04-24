from django.db import migrations

from django.db import migrations

def create_doctors(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('appointments', 'Profile')
    Doctor = apps.get_model('appointments', 'Doctor')

    print("Doctor seeding migration completed. Total doctors:", Doctor.objects.count())

    doctors_data = [
        ("dr_smith", "Cardiologist"),
        ("dr_johnson", "Dentist"),
        ("dr_emily", "Neurologist"),
        ("dr_peter", "Pediatrician"),
        ("dr_sarah", "Dermatologist"),
        ("dr_adam", "Orthopedist"),
        ("dr_ben", "Psychiatrist"),
        ("dr_kate", "Ophthalmologist"),
        ("dr_james", "Gastroenterologist"),
        ("dr_steve", "Urologist"),
        ("dr_lisa", "Cardiology"),
        ("dr_mike", "Neurology"),
    ]

    print("Starting doctor seeding migration...")

    for username, specialization in doctors_data:

        user, _ = User.objects.get_or_create(username=username)

        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={"role": "doctor"}
        )

        doctor, created = Doctor.objects.get_or_create(
            profile=profile,
            defaults={
                "specialization": specialization,
                "availability": {}
            }
        )

        print(f"Doctor {'created' if created else 'already exists'}: {username} ({specialization})")
        
def reverse_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('appointments', 'Profile')
    Doctor = apps.get_model('appointments', 'Doctor')

    for username, _ in [
        ("dr_smith", ""),
        ("dr_johnson", ""),
        ("dr_emily", ""),
        ("dr_peter", ""),
        ("dr_sarah", ""),
        ("dr_adam", ""),
        ("dr_ben", ""),
        ("dr_kate", ""),
        ("dr_james", ""),
        ("dr_steve", ""),
        ("dr_lisa", ""),
        ("dr_mike", ""),
    ]:
        user = User.objects.filter(username=username).first()
        if user:
            profile = Profile.objects.filter(user=user).first()
            if profile:
                Doctor.objects.filter(profile=profile).delete()
                profile.delete()
            user.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_doctors, reverse_func),
    ]
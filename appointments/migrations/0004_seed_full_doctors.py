from django.db import migrations

def create_doctors(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('appointments', 'Profile')
    Doctor = apps.get_model('appointments', 'Doctor')

    doctors_data = [
        ("dr1", "Cardiologist"),
        ("dr2", "Dentist"),
        ("dr3", "Neurologist"),
        ("dr4", "Pediatrician"),
        ("dr5", "Dermatologist"),
        ("dr6", "Orthopedist"),
        ("dr7", "Psychiatrist"),
        ("dr8", "Ophthalmologist"),
        ("dr9", "Gastroenterologist"),
        ("dr10", "Urologist"),
        ("dr11", "Cardiology"),
        ("dr12", "Neurology"),
    ]

    for username, specialization in doctors_data:
        if not User.objects.filter(username=username).exists():

            user = User.objects.create_user(
                username=username,
                password="password123"
            )

            profile = Profile.objects.create(
                user=user,
                role="doctor"
            )

            Doctor.objects.create(
                profile=profile,
                specialization=specialization,
                avatar="https://ui-avatars.com/api/?name=Doctor",
                availability={}
            )

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_seed_doctors'),
    ]

    operations = [
        migrations.RunPython(create_doctors),
    ]
from django.db import migrations

def create_doctors(apps, schema_editor):
    Doctor = apps.get_model('appointments', 'Doctor')

    doctors = [
        "Cardiologist",
        "Dentist",
        "Neurologist",
        "Pediatrician",
        "Dermatologist",
        "Orthopedist",
        "Psychiatrist",
        "Ophthalmologist",
        "Gastroenterologist",
        "Urologist",
        "Cardiology",
        "Neurology",
    ]

    for spec in doctors:
        Doctor.objects.get_or_create(
            specialization=spec,
            defaults={
                "profile_id": 1,  # safe fallback
                "avatar": "https://ui-avatars.com/api/?name=Doctor",
                "availability": {}
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_doctors),
    ]
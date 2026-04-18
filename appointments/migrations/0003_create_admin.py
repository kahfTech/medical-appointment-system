from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin1234'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_seed_doctors'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
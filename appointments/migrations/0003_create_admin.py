from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin(apps, schema_editor):
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="admin1234"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_seed_doctors'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
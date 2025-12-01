from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_projet", "0002_project_is_published"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="created_at",
            new_name="published_at",
        ),
    ]

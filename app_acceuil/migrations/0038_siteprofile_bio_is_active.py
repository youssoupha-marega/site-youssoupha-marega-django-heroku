from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_acceuil", "0037_siteprofile_navbar_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteprofile",
            name="bio_is_active",
            field=models.BooleanField(default=True, verbose_name="Afficher la carte Profil"),
        ),
    ]

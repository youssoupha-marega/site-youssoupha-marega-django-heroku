from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_acceuil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='show_chip',
            field=models.BooleanField(default=True, verbose_name='Afficher le chip utilisateur'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='chip_text',
            field=models.CharField(blank=True, max_length=100, verbose_name='Texte du chip (override)'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='chip_use_photo',
            field=models.BooleanField(default=True, verbose_name="Utiliser la photo dans le chip"),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='chip_shape',
            field=models.CharField(choices=[('circle','Circle'),('square','Square')], default='circle', max_length=10, verbose_name='Forme du chip'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='chip_color',
            field=models.CharField(default='#0d6efd', max_length=20, verbose_name='Couleur du chip'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='chip_title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Titre affiché au côté du chip'),
        ),
    ]

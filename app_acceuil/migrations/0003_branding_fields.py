from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_acceuil', '0002_add_chip_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='site_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='Titre du site (balise <title>)'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to='favicon/', verbose_name='Favicon'),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='navbar_avatar_shape',
            field=models.CharField(choices=[('circle','Circle'),('square','Square'),('none','No frame')], default='circle', max_length=10, verbose_name='Forme avatar navbar'),
        ),
    ]

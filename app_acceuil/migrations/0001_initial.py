from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=150, verbose_name='Nom')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Localisation')),
                ('profession', models.CharField(blank=True, max_length=255, verbose_name='Profession')),
                ('current_employer', models.CharField(blank=True, max_length=255, verbose_name='Employeur actuel')),
                ('current_employer_url', models.URLField(blank=True, verbose_name='Lien employeur')),
                ('linkedin_url', models.URLField(blank=True, verbose_name='LinkedIn')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Adresse email')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Photo de profil')),
                ('bio', ckeditor.fields.RichTextField(blank=True, verbose_name='Profil (rich text)')),
            ],
            options={
                'verbose_name': 'Profil du site',
                'verbose_name_plural': 'Profil du site',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titre de la formation')),
                ('date', models.CharField(blank=True, max_length=100, verbose_name='Date / Années')),
                ('institution', models.CharField(blank=True, max_length=255, verbose_name='Établissement')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('profile', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='educations', to='app_acceuil.siteprofile')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Formation',
                'verbose_name_plural': 'Formations',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Intitulé / Poste')),
                ('date', models.CharField(blank=True, max_length=100, verbose_name='Date / Période')),
                ('company', models.CharField(blank=True, max_length=255, verbose_name='Entreprise')),
                ('company_url', models.URLField(blank=True, verbose_name='Lien entreprise')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('profile', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='experiences', to='app_acceuil.siteprofile')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Expérience',
                'verbose_name_plural': 'Expériences',
            },
        ),
    ]

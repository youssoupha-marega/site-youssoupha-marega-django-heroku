# Generated manually to remove legacy ManyToMany fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_acceuil', '0037_siteprofile_navbar_position'),
    ]

    operations = [
        # Remove all legacy ManyToMany fields that referenced deleted apps
        migrations.RemoveField(
            model_name='siteprofile',
            name='published_projects',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='featured_projects',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='published_articles',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='featured_articles',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='published_services',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='featured_services',
        ),
    ]

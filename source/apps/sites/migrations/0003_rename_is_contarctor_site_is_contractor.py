# Generated by Django 5.1.1 on 2024-10-15 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_site_is_contarctor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='is_contarctor',
            new_name='is_contractor',
        ),
    ]

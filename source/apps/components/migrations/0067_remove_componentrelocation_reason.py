# Generated by Django 5.1.1 on 2025-01-25 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0066_componentattachment_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componentrelocation',
            name='reason',
        ),
    ]

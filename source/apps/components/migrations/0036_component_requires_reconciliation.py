# Generated by Django 5.1.1 on 2024-10-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0035_alter_componenttask_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='requires_reconciliation',
            field=models.BooleanField(blank=True, null=True, verbose_name='Требует сверки'),
        ),
    ]

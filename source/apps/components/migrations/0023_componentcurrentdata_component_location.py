# Generated by Django 5.1.1 on 2024-10-14 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0022_alter_componentcurrentdata_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentcurrentdata',
            name='component_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='component', to='components.componentinstallationlocation', verbose_name='Место установки'),
        ),
    ]

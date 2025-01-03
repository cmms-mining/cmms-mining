# Generated by Django 5.1.1 on 2024-12-29 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0059_componentrepair_contractor'),
        ('contractors', '0008_quotation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentrepair',
            name='appendix',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairs', to='contractors.appendix', verbose_name='Приложение к договору'),
        ),
        migrations.AddField(
            model_name='componentrepair',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairs', to='contractors.contract', verbose_name='Договор'),
        ),
    ]

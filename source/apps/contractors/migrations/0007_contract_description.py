# Generated by Django 5.1.1 on 2024-12-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0006_appendix_components_contract_components'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание'),
        ),
    ]

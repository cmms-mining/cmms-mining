# Generated by Django 5.1.1 on 2024-12-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0051_alter_componentrelocation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='is_compliant_with_accounting',
            field=models.BooleanField(default=False, verbose_name='Соответствует бухгалтерскому учету'),
        ),
    ]

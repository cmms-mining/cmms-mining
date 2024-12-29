# Generated by Django 5.1.1 on 2024-12-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0008_quotation_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appendix',
            name='components',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='components',
        ),
        migrations.AlterField(
            model_name='contract',
            name='date',
            field=models.DateField(default="2024-01-01", verbose_name='Дата'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1.1 on 2024-12-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0002_alter_appendix_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование'),
        ),
    ]
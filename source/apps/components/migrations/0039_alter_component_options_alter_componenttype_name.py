# Generated by Django 5.1.1 on 2024-10-18 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0038_componenttype_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['component_type'], 'verbose_name': 'Компонент', 'verbose_name_plural': '(Справочник) Компоненты'},
        ),
        migrations.AlterField(
            model_name='componenttype',
            name='name',
            field=models.CharField(max_length=60, unique=True, verbose_name='Наименование'),
        ),
    ]

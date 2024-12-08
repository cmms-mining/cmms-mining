# Generated by Django 5.1.1 on 2024-11-03 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0045_componentcurrentdata_installation_date'),
        ('equipments', '0018_rename_last_edit_by_equipmentcurrentdata_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Статус компонента',
                'verbose_name_plural': 'Статусы компонентов',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='componentcurrentdata',
            name='component_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='components.componentinstallationlocation', verbose_name='Место установки'),
        ),
        migrations.AlterField(
            model_name='componentcurrentdata',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='equipments.equipment', verbose_name='Оборудование'),
        ),
        migrations.AddField(
            model_name='componentcurrentdata',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='components.componentstate', verbose_name='Состояние'),
        ),
    ]

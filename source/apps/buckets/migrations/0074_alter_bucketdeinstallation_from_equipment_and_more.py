# Generated by Django 5.1.1 on 2024-10-03 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0073_alter_bucketdeinstallation_reason_and_more'),
        ('equipments', '0009_alter_nameplate_attachment_file_and_more'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketdeinstallation',
            name='from_equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='equipments.equipment', verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='bucketinstallation',
            name='to_equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='equipments.equipment', verbose_name='Куда'),
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='from_site',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss_from_site', to='sites.site', verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='to_site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss_to_site', to='sites.site', verbose_name='Куда'),
        ),
    ]

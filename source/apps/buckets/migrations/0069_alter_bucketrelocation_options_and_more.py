# Generated by Django 5.1.1 on 2024-10-03 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0068_alter_bucketreconciliation_date'),
        ('common', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bucketrelocation',
            options={'verbose_name': 'Перемещение ковша', 'verbose_name_plural': 'Перемещения ковшей'},
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='from_site',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='relocations_from_site', to='sites.site', verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.relocationreason', verbose_name='Причина'),
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='to_site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relocations_to_site', to='sites.site', verbose_name='Куда'),
        ),
        migrations.AlterField(
            model_name='historicalbucketrelocation',
            name='reason',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='common.relocationreason', verbose_name='Причина'),
        ),
    ]
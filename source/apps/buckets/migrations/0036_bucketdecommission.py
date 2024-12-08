# Generated by Django 5.1.1 on 2024-09-09 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0035_historicalbucket_delete_historicalbucketcapacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketDecommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obsoleted', models.BooleanField(default=False, verbose_name='Выведен из эксплуатации')),
                ('obsoleted_date', models.DateField(blank=True, null=True, verbose_name='Дата вывода из эксплуатации')),
                ('decommissioned', models.BooleanField(default=False, verbose_name='Списан')),
                ('decommissioned_date', models.DateField(blank=True, null=True, verbose_name='Дата списания')),
                ('bucket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='decommission', to='buckets.bucket', verbose_name='Ковш')),
            ],
            options={
                'verbose_name': 'Списание ковша',
                'verbose_name_plural': 'Списания ковшей',
                'ordering': ['bucket'],
            },
        ),
    ]

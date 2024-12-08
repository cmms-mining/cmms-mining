# Generated by Django 5.1.1 on 2024-09-07 06:02

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0025_alter_bucket_number_alter_bucket_production_year'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketTechState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата техсостояния')),
                ('techstate', models.CharField(choices=[('Требует текущего ремонта', 'Требует текущего ремонта'), ('Требует капитального ремонта', 'Требует капитального ремонта'), ('Ремонта не требует', 'Ремонта не требует')], max_length=100, verbose_name='Техсостояние')),
                ('is_operable', models.BooleanField(default=True, verbose_name='Подлежит эксплуатации')),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='techstates', to='buckets.bucket', verbose_name='Ковш')),
            ],
            options={
                'verbose_name': 'Техсостояние ковша',
                'verbose_name_plural': 'Техсостояния ковшей',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalBucketTechState',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата техсостояния')),
                ('techstate', models.CharField(choices=[('Требует текущего ремонта', 'Требует текущего ремонта'), ('Требует капитального ремонта', 'Требует капитального ремонта'), ('Ремонта не требует', 'Ремонта не требует')], max_length=100, verbose_name='Техсостояние')),
                ('is_operable', models.BooleanField(default=True, verbose_name='Подлежит эксплуатации')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bucket', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='buckets.bucket', verbose_name='Ковш')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Техсостояние ковша',
                'verbose_name_plural': 'historical Техсостояния ковшей',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

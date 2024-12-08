# Generated by Django 5.1.1 on 2024-10-12 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logger_name', models.CharField(max_length=100)),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'NotSet'), (20, 'Info'), (30, 'Warning'), (10, 'Debug'), (40, 'Error'), (50, 'Fatal')], db_index=True, default=40)),
                ('msg', models.TextField()),
                ('trace', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Logging',
                'verbose_name_plural': 'Logging',
                'ordering': ('-create_at',),
            },
        ),
    ]

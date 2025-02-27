# Generated by Django 4.1.7 on 2024-08-30 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0009_alter_bucketrelocation_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='number',
            field=models.CharField(blank=True, max_length=3, null=True, unique=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='bucketrelocation',
            name='bucket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relocations', to='buckets.bucket', verbose_name='Ковш'),
        ),
    ]

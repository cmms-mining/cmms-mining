# Generated by Django 4.1.7 on 2024-08-26 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0006_bucketreceiving_init_sending'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketRelocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_side', models.CharField(max_length=30, verbose_name='Откуда')),
                ('to_side', models.CharField(max_length=30, verbose_name='Куда')),
                ('send_date', models.DateField(blank=True, null=True, verbose_name='Дата отправки')),
                ('receive_date', models.DateField(blank=True, null=True, verbose_name='Дата получения')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending', to='buckets.bucket', verbose_name='Ковш')),
            ],
            options={
                'verbose_name': 'Перемещение ковша',
                'verbose_name_plural': 'Перемещения ковшей',
                'ordering': ['send_date'],
            },
        ),
        migrations.RemoveField(
            model_name='bucketsending',
            name='bucket',
        ),
        migrations.DeleteModel(
            name='BucketReceiving',
        ),
        migrations.DeleteModel(
            name='BucketSending',
        ),
    ]
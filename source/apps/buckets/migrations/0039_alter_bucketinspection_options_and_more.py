# Generated by Django 5.1.1 on 2024-09-16 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0038_alter_bucketrelocation_received_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bucketinspection',
            options={'ordering': ['-date'], 'verbose_name': 'Инспекция ковша', 'verbose_name_plural': 'Инспекции ковшей'},
        ),
        migrations.AlterModelOptions(
            name='bucketreconciliation',
            options={'ordering': ['-date'], 'verbose_name': 'Сверка данных ковша', 'verbose_name_plural': 'Сверки данных ковша'},
        ),
        migrations.AlterModelOptions(
            name='bucketrelocation',
            options={'ordering': ['-date'], 'verbose_name': 'Перемещение ковша', 'verbose_name_plural': 'Перемещения ковшей'},
        ),
        migrations.AlterModelOptions(
            name='buckettechstate',
            options={'ordering': ['-date'], 'verbose_name': 'Техсостояние ковша', 'verbose_name_plural': 'Техсостояния ковшей'},
        ),
    ]
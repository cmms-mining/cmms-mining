# Generated by Django 5.1.1 on 2024-12-25 18:40

import apps.common.services
import apps.contractors.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0003_alter_contractor_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appendixattachment',
            options={'verbose_name': 'Вложение для приложения к контракту', 'verbose_name_plural': 'Вложения для приложений к контрактам'},
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('description', models.CharField(max_length=200, unique=True, verbose_name='Описание')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations', to='contractors.contractor', verbose_name='Контрагент')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment_file', models.FileField(upload_to=apps.contractors.models.appendix_attachment_upload_path, validators=[apps.common.services.validate_scan_file], verbose_name='Файл')),
                ('file_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='Размер файла')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='contractors.quotation', verbose_name='Коммерческое предложение')),
            ],
            options={
                'verbose_name': 'Вложение для коммерческого предложения',
                'verbose_name_plural': 'Вложения для коммерческих предложений',
            },
        ),
    ]
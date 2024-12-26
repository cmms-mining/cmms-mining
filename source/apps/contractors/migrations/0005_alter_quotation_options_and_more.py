# Generated by Django 5.1.1 on 2024-12-26 11:55

import apps.common.services
import apps.contractors.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0059_componentrepair_contractor'),
        ('contractors', '0004_alter_appendixattachment_options_quotation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quotation',
            options={'ordering': ['date'], 'verbose_name': 'Коммерческое предложение', 'verbose_name_plural': 'Коммерческие предложения'},
        ),
        migrations.AlterModelOptions(
            name='quotationattachment',
            options={'verbose_name': 'Вложение для КП', 'verbose_name_plural': 'Вложения для КП'},
        ),
        migrations.AddField(
            model_name='quotation',
            name='components',
            field=models.ManyToManyField(blank=True, related_name='quotations', to='components.component', verbose_name='Компоненты'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='date',
            field=models.DateField(default='2024-01-01', verbose_name='Дата'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationattachment',
            name='attachment_file',
            field=models.FileField(upload_to=apps.contractors.models.quotation_attachment_upload_path, validators=[apps.common.services.validate_scan_file], verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='quotationattachment',
            name='quotation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='contractors.quotation', verbose_name='КП'),
        ),
    ]

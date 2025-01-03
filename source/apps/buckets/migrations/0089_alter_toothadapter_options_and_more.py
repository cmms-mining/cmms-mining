# Generated by Django 5.1.1 on 2024-10-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0088_delete_historicalbucketrelocationattachment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toothadapter',
            options={'ordering': ['name'], 'verbose_name': 'Адаптер коронки', 'verbose_name_plural': '(Справочник) Адаптеры коронок'},
        ),
        migrations.AddField(
            model_name='bucketcurrentdata',
            name='relocation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата перемещения'),
        ),
        migrations.AddField(
            model_name='bucketcurrentdata',
            name='techstate_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата техсостояния'),
        ),
    ]

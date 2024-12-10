# Generated by Django 5.1.1 on 2024-11-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0031_alter_relocationattachment_equipment_relocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='relocationorder',
            name='status',
            field=models.CharField(choices=[('waiting', 'В ожидании актов'), ('completed', 'Выполнен'), ('invalid', 'Недействителен')], default='generic', max_length=20, verbose_name='Статус'),
        ),
    ]
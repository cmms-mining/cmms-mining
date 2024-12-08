# Generated by Django 4.1.7 on 2023-05-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0002_remove_equipment_equipment_attachment_group'),
        ('equip_documents', '0006_equipmentattachmentgroup_equipments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentattachmentgroup',
            name='equipments',
        ),
        migrations.AddField(
            model_name='equipmentattachmentgroup',
            name='equipments',
            field=models.ManyToManyField(blank=True, related_name='equipment_attachment_groups', to='equipments.equipment', verbose_name='Оборудование'),
        ),
    ]

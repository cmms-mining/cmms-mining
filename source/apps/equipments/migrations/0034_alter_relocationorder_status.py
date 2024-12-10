# Generated by Django 5.1.1 on 2024-12-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0033_alter_relocationorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relocationorder',
            name='status',
            field=models.CharField(choices=[('waiting', 'В ожидании актов'), ('completed', 'Выполнен'), ('invalid', 'Отменен')], default='waiting', max_length=20, verbose_name='Статус'),
        ),
    ]
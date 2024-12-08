# Generated by Django 5.1.1 on 2024-11-23 18:59

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0022_relocationorder_equipments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='relocationorder',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='authored_orders', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relocationorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relocationorder',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата редактирования'),
        ),
        migrations.AddField(
            model_name='relocationorder',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_last_edited', to=settings.AUTH_USER_MODEL, verbose_name='Последний редактор'),
        ),
        migrations.AlterField(
            model_name='relocationorder',
            name='equipments',
            field=models.ManyToManyField(blank=True, related_name='orders', to='equipments.equipment', verbose_name='Оборудование'),
        ),
    ]

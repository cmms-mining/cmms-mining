# Generated by Django 4.1.7 on 2023-05-09 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("equipments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EventType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип событий",
                "verbose_name_plural": "Типы событий",
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("date", models.DateField(blank=True, null=True, verbose_name="Дата")),
                ("time", models.TimeField(blank=True, null=True, verbose_name="Время")),
                (
                    "note",
                    models.TextField(blank=True, null=True, verbose_name="Примечание"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "equipments",
                    models.ManyToManyField(
                        blank=True,
                        related_name="events",
                        to="equipments.equipment",
                        verbose_name="Оборудования",
                    ),
                ),
                (
                    "event_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.eventtype",
                        verbose_name="Тип события",
                    ),
                ),
            ],
            options={
                "verbose_name": "Событие",
                "verbose_name_plural": "События",
            },
        ),
    ]

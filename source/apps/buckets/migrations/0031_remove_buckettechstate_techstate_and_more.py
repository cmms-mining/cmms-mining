# Generated by Django 5.1.1 on 2024-09-08 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0030_alter_buckettechstate_techstate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buckettechstate',
            name='techstate',
        ),
        migrations.RemoveField(
            model_name='historicalbuckettechstate',
            name='techstate',
        ),
    ]
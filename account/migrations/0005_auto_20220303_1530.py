# Generated by Django 3.1 on 2022-03-03 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220303_0155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='time',
            new_name='time_of_queue_entry',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='timezone',
        ),
    ]

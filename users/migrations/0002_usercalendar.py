# Generated by Django 3.1 on 2022-03-03 00:55

import core.common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220303_0155'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('activated_at', models.DateTimeField(blank=True, null=True)),
                ('deactivated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mo_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('mo_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('tu_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('tu_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('we_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('we_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('th_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('th_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('fr_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('fr_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('sa_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('sa_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('su_o', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('su_c', core.common.fields.DefaultTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='calendar', to='account.userprofile')),
            ],
            options={
                'verbose_name': '[User Profile] Calendar',
                'ordering': ['-created_at'],
            },
        ),
    ]

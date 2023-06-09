# Generated by Django 3.2.13 on 2023-05-02 08:31

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20230502_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nurses',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='hours_available',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='mobile_number',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='other_name',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='skill_level',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='surname',
        ),
        migrations.AddField(
            model_name='nurses',
            name='assignments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nurses',
            name='nurse_id',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17')], default=1, unique=True),
        ),
        migrations.AddField(
            model_name='nurses',
            name='shift_type',
            field=models.CharField(choices=[('day', 'Day'), ('night', 'Night')], default=backend.models.Days, max_length=200),
        ),
    ]

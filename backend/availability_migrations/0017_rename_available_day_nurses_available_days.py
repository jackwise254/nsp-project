# Generated by Django 3.2.13 on 2023-05-03 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20230503_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nurses',
            old_name='available_day',
            new_name='available_days',
        ),
    ]

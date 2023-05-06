# Generated by Django 3.2.13 on 2023-05-04 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_nurses_available_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nurses',
            name='available_days',
        ),
        migrations.AlterField(
            model_name='nurses',
            name='shift_type',
            field=models.CharField(choices=[('day', 'Day'), ('night', 'Night')], default='day', max_length=200),
        ),
    ]

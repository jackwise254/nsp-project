# Generated by Django 3.2.13 on 2023-04-20 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_shifts_shifttime'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shiftassignment',
            unique_together={('nurse', 'shift')},
        ),
    ]

# Generated by Django 3.2.13 on 2023-04-20 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20230420_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurses',
            name='hours_available',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='nurses',
            name='skill_level',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]

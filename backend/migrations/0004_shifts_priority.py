# Generated by Django 3.2.13 on 2023-04-20 06:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20230420_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifts',
            name='priority',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
# Generated by Django 3.2.13 on 2023-05-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_auto_20230504_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurses',
            name='available_days',
            field=models.ManyToManyField(to='backend.Days'),
        ),
    ]

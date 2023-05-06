# Generated by Django 3.2.13 on 2023-05-04 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_nurses_available_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurses',
            name='hours_available',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

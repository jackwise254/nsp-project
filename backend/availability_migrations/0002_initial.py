# Generated by Django 3.2.13 on 2023-04-20 09:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0001_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
            ],
        ),
        migrations.CreateModel(
            name='Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Nurses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('other_name', models.CharField(blank=True, max_length=200)),
                ('mobile_number', models.IntegerField(blank=True)),
                ('hours_available', models.IntegerField(blank=True, default=1)),
                ('skill_level', models.IntegerField(blank=True, default=1)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10)),
                ('available_days', models.ManyToManyField(to='backend.Availability')),
            ],
        ),
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeinterval', models.CharField(blank=True, max_length=200)),
                ('shifttype', models.CharField(blank=True, max_length=200)),
                ('constraints', models.CharField(choices=[('soft', 'Soft'), ('Hard', 'hard')], default='soft', max_length=200)),
                ('penalty_cost', models.IntegerField(choices=[(20, 20), (10, 10)], default=20)),
                ('priority', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.nurses')),
            ],
        ),
        migrations.AddField(
            model_name='availability',
            name='nurse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.nurses'),
        ),
    ]

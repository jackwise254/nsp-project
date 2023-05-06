# Generated by Django 3.2.13 on 2023-05-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_alter_nurses_nurse_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nurses',
            name='assignments',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='nurse_id',
        ),
        migrations.RemoveField(
            model_name='nurses',
            name='shift_type',
        ),
        migrations.RemoveField(
            model_name='shifts',
            name='coverage_demand',
        ),
        migrations.AddField(
            model_name='nurses',
            name='firstname',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nurses',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        ),
        migrations.AddField(
            model_name='nurses',
            name='hours_available',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='nurses',
            name='mobile_number',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nurses',
            name='other_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='nurses',
            name='skill_level',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='nurses',
            name='surname',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shifts',
            name='constraints',
            field=models.CharField(choices=[('soft', 'Soft'), ('Hard', 'hard')], default='soft', max_length=200),
        ),
        migrations.AlterField(
            model_name='shifts',
            name='shifttype',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

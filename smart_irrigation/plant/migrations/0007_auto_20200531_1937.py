# Generated by Django 3.0.5 on 2020-05-31 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0006_plant_irrigation_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='last_irrigation_date',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last Irrigation Date'),
        ),
    ]

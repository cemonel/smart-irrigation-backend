# Generated by Django 3.0.5 on 2020-05-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='last_irrigation_date',
            field=models.DateTimeField(blank=True, default=None, verbose_name='Date'),
        ),
    ]
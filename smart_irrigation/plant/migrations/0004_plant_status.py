# Generated by Django 3.0.5 on 2020-05-10 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0003_auto_20200504_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='status',
            field=models.CharField(choices=[('wait', 'Wait'), ('irrigate', 'Irriate')], default='wait', max_length=10),
        ),
    ]

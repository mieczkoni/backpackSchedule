# Generated by Django 2.1.3 on 2018-11-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='hours',
            field=models.IntegerField(default=0),
        ),
    ]

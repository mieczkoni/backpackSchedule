# Generated by Django 2.1.3 on 2018-11-26 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20181126_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrating',
            name='subject_rating',
            field=models.IntegerField(default=0),
        ),
    ]

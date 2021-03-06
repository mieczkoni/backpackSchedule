# Generated by Django 2.1.3 on 2019-01-08 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_usersubject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubject',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Subject'),
        ),
        migrations.AlterField(
            model_name='usersubject',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

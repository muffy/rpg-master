# Generated by Django 2.0.5 on 2018-05-15 01:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20180515_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_time',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 7, 0)),
        ),
    ]
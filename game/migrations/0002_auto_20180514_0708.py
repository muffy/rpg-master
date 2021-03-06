# Generated by Django 2.0.5 on 2018-05-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adjustment',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='encounter',
            options={'ordering': ['-first_round']},
        ),
        migrations.AlterModelOptions(
            name='encountercharacter',
            options={'ordering': ['-initiative']},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='gameadjustment',
            options={'ordering': ['-start_round']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='character',
            name='emoji',
            field=models.CharField(default=':smiling:', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameadjustment',
            name='duration',
            field=models.IntegerField(default=-1),
        ),
    ]

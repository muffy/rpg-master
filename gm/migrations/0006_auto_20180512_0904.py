# Generated by Django 2.0.5 on 2018-05-12 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gm', '0005_gamecharacters'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EncounterCharacters',
            new_name='EncounterCharacter',
        ),
        migrations.RenameModel(
            old_name='GameAdjustments',
            new_name='GameAdjustment',
        ),
        migrations.RenameModel(
            old_name='GameCharacters',
            new_name='GameCharacter',
        ),
    ]
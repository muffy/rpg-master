from django.db import models


class Player(models.Model):
    slack_id = models.CharField(max_length=20,unique=True)

    class Meta:
        db_table = 'player'


# This can represent either a player character or an NPC
#  - (enemy) NPCs belong to the Player who is also the GM
#  - Generally for PCs, hit points and CMD will not be relevant (for the bot)
class Character(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    initiative_modifier = models.IntegerField(default=0)
    perception_modifier = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=10)
    hit_points = models.IntegerField(default=0)
    cmd = models.IntegerField(default=10)

    class Meta:
        db_table = 'character'


# For now, there should be one game per slack channel; we will make this more flexible later.
class Game(models.Model):
    name = models.CharField(max_length=200)
    ended = models.BooleanField(default=False)
    gm = models.ForeignKey(Player, on_delete=models.CASCADE)
    slack_channel = models.CharField(max_length=20,null=True)

    class Meta:
        db_table = 'game'


# For one, one encounter should be running at a time.
class Encounter(models.Model):
    name = models.CharField(max_length=200)
    ended = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        db_table = 'encounter'


# Details of an encounter - which characters, initiative, delay status, readied status, conditions, etc.
class EncounterCharacters(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    initiative = models.IntegerField(default=0)
    delaying = models.BooleanField(default=False)

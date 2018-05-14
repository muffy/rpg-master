from django.db import models
from django.contrib.postgres import fields

class Player(models.Model):
    slack_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.slack_id})"

    class Meta:
        db_table = 'player'
        ordering = ['name']

# This can represent either a player character or an NPC
#  - (enemy) NPCs belong to the Player who is also the GM
#  - Generally for PCs, hit points, CMD, and saves will not be relevant (for the bot)
#    However, players who will not be around can ask the bot to roll saves for them.
class Character(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    stats = fields.JSONField(default=dict())
    statblock = models.TextField()
    emoji = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.player.name})"

    class Meta:
        db_table = 'character'
        ordering = ['name']


# For now, there should be one game per slack channel; we will make this more flexible later.
class Game(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    gm = models.ForeignKey(Player, on_delete=models.CASCADE)
    slack_channel = models.CharField(max_length=20, null=False)
    current_round = models.IntegerField(default=0)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'game'
        ordering = ['name']


# For one, one encounter should be running at a time.
class Encounter(models.Model):
    name = models.CharField(max_length=200)
    ended = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    first_round = models.IntegerField(default=1)
    characters = models.ManyToManyField(Character, through='EncounterCharacter')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'encounter'
        ordering = ['-first_round']


# Buffs, debuffs, spells, etc.
class Adjustment(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return f'<a href="{self.url}">{self.name}</a>'

    class Meta:
        db_table = 'adjustment'
        ordering = ['name']


# Adjustments which are active in a game at the moment
class GameAdjustment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    adjustment = models.ForeignKey(Adjustment, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)
    source = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, related_name='source')
    start_round = models.IntegerField(default=0)
    duration = models.IntegerField(default=-1)

    class Meta:
        db_table = 'game_adjustment'
        ordering = ['-start_round']


# Details of an encounter - which characters, initiative, delay status, readied status, conditions, etc.
class EncounterCharacter(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    initiative = models.IntegerField(default=0)
    delaying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character.name} ({self.initiative})"

    class Meta:
        db_table = 'encounter_character'
        ordering = ['-initiative']

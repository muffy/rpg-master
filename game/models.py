from django.db import models
from django.contrib.postgres import fields
from django.contrib.auth.admin import User

from datetime import datetime, timedelta

DEFAULT_GAME_START = datetime.min + timedelta(hours=7)

class Player(models.Model):
    slack_id = models.CharField(max_length=20,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} ({self.slack_id})"

    class Meta:
        db_table = 'player'

# This can represent either a player character or an NPC
#  - (enemy) NPCs belong to the Player who is also the GM
class Character(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    nicknames = fields.ArrayField(models.CharField(max_length=20), default=list())
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_channel = models.CharField(max_length=20, null=False)
    characters = models.ManyToManyField(Character)
    game_time = models.DateTimeField(default=DEFAULT_GAME_START)

    def __str__(self):
        return self.name

    def day(self):
        return (self.game_time - datetime.min).days

    def day_and_time(self):
        return f"{self.game_time.hour:0>2}:{self.game_time.minute:0>2}:{self.game_time.second:0>2} on day {self.day()}"

    class Meta:
        db_table = 'game'
        ordering = ['name']


# For one, one encounter should be running at a time.
class Encounter(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character, through='EncounterCharacter')
    encounter_time = models.DateTimeField(default=datetime.min)
    round = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'encounter'
        ordering = ['-encounter_time']


# Buffs, debuffs, spells, etc.
class Adjustment(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return f'{self.name}: {self.url}'

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

    def __str__(self):
        names = ', '.join([character.name for character in self.characters.all()])
        return f"{self.adjustment.name}: {names}"

    class Meta:
        db_table = 'game_adjustment'
        ordering = ['-start_round']


# Details of an encounter - which characters, initiative, delay status, readied status, conditions, etc.
class EncounterCharacter(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    initiative = models.IntegerField(default=0)
    delaying = models.BooleanField(default=False)
    last_acted = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.character.name} ({self.initiative})"

    class Meta:
        db_table = 'encounter_character'
        ordering = ['-initiative']

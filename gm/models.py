from django.db import models


class Player(models.Model):
    slack_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name or self.slack_id}"

    class Meta:
        db_table = 'player'


# This can represent either a player character or an NPC
#  - (enemy) NPCs belong to the Player who is also the GM
#  - Generally for PCs, hit points, CMD, and saves will not be relevant (for the bot)
#    However, players who will not be around can ask the bot to roll saves for them.
class Character(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    initiative_modifier = models.IntegerField(default=0)
    perception_modifier = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=10)
    hit_points = models.IntegerField(default=0)
    cmd = models.IntegerField(default=10)
    will_save = models.IntegerField(default=0)
    reflex_save = models.IntegerField(default=0)
    fortitude_save = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'character'


# For now, there should be one game per slack channel; we will make this more flexible later.
class Game(models.Model):
    name = models.CharField(max_length=200)
    ended = models.BooleanField(default=False)
    gm = models.ForeignKey(Player, on_delete=models.CASCADE)
    slack_channel = models.CharField(max_length=20,null=True)
    current_round = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'game'


# For one, one encounter should be running at a time.
class Encounter(models.Model):
    name = models.CharField(max_length=200)
    ended = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_round = models.IntegerField(default=0) # this is the game round in which the encounter started

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'encounter'


# Details of an encounter - which characters, initiative, delay status, readied status, conditions, etc.
class EncounterCharacters(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    initiative = models.IntegerField(default=0)
    delaying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character.name} ({self.initiative})"

    class Meta:
        db_table = 'encounter_characters'


# Buffs, debuffs, spells, etc.
class Adjustment(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'adjustment'


# Adjustments which are active in a game at the moment
# These can be just to the game or they can be active during a particular encounter or on a character or characters
class GameAdjustments(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, null=True)
    character =  models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    adjustment =  models.ForeignKey(Adjustment, on_delete=models.CASCADE)
    start_round = models.IntegerField(default=0)
    end_round = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.character.name}: {self.adjustment.name}"

    class Meta:
        db_table = 'game_adjustments'
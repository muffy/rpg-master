from django.db import models


class Player(models.Model):
    slack_id = models.CharField(max_length=20,unique=True)

    class Meta:
        db_table = 'player'


class PlayerCharacter(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    initiative_modifier = models.IntegerField(default=0)
    perception_modifier = models.IntegerField(default=0)

    class Meta:
        db_table = 'player_character'


class Game(models.Model):
    name = models.CharField(max_length=200)
    gm = models.ForeignKey(Player, on_delete=models.CASCADE)
    slack_channel = models.CharField(max_length=20,null=True)
    current = models.BooleanField(default=True)
    players = models.ManyToManyField(Player,
                                     related_name="%(class)s_players",
                                     related_query_name="players")
    player_characters = models.ManyToManyField(PlayerCharacter,
                                               related_name="%(class)s_player_characters",
                                               related_query_name="player_characters")

    class Meta:
        db_table = 'game'

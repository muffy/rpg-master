from pyparsing import *

"""
Commands

Game

  "create game giantslayer"
  "start game giantslayer"

  create := 'create' | 'new' | 'add' | 'make'
  select := 'select' | 'choose' | 'start'
  action := create | select
  name := (alpha,nums,'-_')+
  game := action + 'game' + name
  
Player Character (PC)

  "add Gwen and Carl [to giantslayer]" (from @Megan (Player))
  "add :troll:Hal [to [game] giantslayer] at initiative/init 22+3" (from @Muffy (GM))
  "set Gwen's initiative/init bonus/modifier/mod to [+/-]1"
  "set Gwen's perception bonus/modifier/mod to [+/-]1"
  "set Gwen's initiative to 23[+1]"
  "roll initiative"
  
  join := 'join' | 'play'
  
"""

ACTION_WORDS = {
    'create': ['create', 'new'],
    'join': ['join', 'play'],
    'select': ['select', 'choose', 'start']
}

NAME_CHARS = alphanums + '-_'
GAME_ACTION_WORDS = ACTION_WORDS['create'] + ACTION_WORDS['select'] + ACTION_WORDS['join']

GAME_ACTION = oneOf(' '.join(GAME_ACTION_WORDS))('action')
NAME = Word(NAME_CHARS)('name')

GAME_COMMAND = GAME_ACTION + Optional(Keyword('game'), 'game') + NAME
PC_COMMAND = 'TODO'

COMMAND = Or(GAME_COMMAND, PC_COMMAND)


def parse_message(text):
    return [(canonicalize_action(match[0].action, 'game'), match[0].name) for match in GAME_COMMAND.scanString(text)][0]


def canonicalize_action(action, subject):
    for canonical_action in ACTION_WORDS.keys():
        if action in ACTION_WORDS[canonical_action]:
            return f"{canonical_action}_{subject}"

    return None

from pyparsing import *

"""
Commands

Game

  "create game giantslayer"
  "start game giantslayer"
  "join game giantslayer"

  create := 'create' | 'new' | 'add' | 'make'
  select := 'select' | 'choose' | 'start'
  join := 'join' | 'play'
  action := create | select | join
  name := (alpha,nums,'-_')+
  game := action + 'game' + name
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

GAME_COMMAND = GAME_ACTION + Keyword('game') + NAME


def parse_message(text):
    return [(canonicalize_action(match[0].action), match[0].name) for match in GAME_COMMAND.scanString(text)][0]


def canonicalize_action(action):
    for canonical_action in ACTION_WORDS.keys():
        if action in ACTION_WORDS[canonical_action]:
            return canonical_action

    return None

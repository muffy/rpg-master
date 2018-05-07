from gm.models import Game

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from slackclient import SlackClient

from os import environ

from messageparser import parse_message

SLACK_VERIFICATION_TOKEN = environ.get('SLACK_VERIFICATION_TOKEN')
SLACK_BOT_USER_TOKEN = environ.get('SLACK_BOT_USER_TOKEN')
Client = SlackClient(SLACK_BOT_USER_TOKEN)


class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        print(slack_message)

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data={'challenge': slack_message.get('challenge'),
                                  'type': 'url_verification'},
                            status=status.HTTP_200_OK)

        # see if it's a message to the bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # ignore bot's own message
            if event_message.get('subtype') != 'bot_message':
                self.parse_message(event_message)

        return Response(status=status.HTTP_200_OK)

    def parse_message(self, event_message):
        user = event_message.get('user')
        text = event_message.get('text')
        channel = event_message.get('channel')

        action, name = parse_message(text)

        print(f"{action} game {name}")

        response_text = ":robot: I'm afraid I can't do that, <@{}>".format(user)

        Client.api_call(method='chat.postMessage', channel=channel, text=response_text)


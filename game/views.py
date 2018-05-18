from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Game

from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')


def index(request):
    games = Game.objects.all
    return render(
        request,
        'game/index.html',
        context={'games': games}
    )

class GameDetailView(DetailView):
    model = Game


from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Game

from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')


class GameListView(ListView):
    model = Game
    paginate_by = 100


class GameDetailView(DetailView):
    model = Game


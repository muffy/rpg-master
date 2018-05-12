from django.urls import path

from . import views

app_name = 'gm'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
]
from django.conf.urls import include, url
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='detail'),
]
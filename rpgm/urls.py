from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin

from api.views import Api                                    #

admin.autodiscover()

import game.views

urlpatterns = [
    url(r'^$', game.views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('game/', include('game.urls')),
    url(r'^api/', Api.as_view())
]

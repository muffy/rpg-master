from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin

from api.views import Api                                    #

admin.autodiscover()

import gm.views

urlpatterns = [
    url(r'^$', gm.views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('gm/', include('gm.urls')),
    url(r'^api/', Api.as_view())
]

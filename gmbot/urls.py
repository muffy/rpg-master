from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin

from events.views import Events                                    #

admin.autodiscover()

import gm.views

# Examples:
# url(r'^$', 'gmbot.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
#    url(r'^db', gm.views.db, name='db'),

urlpatterns = [
    url(r'^$', gm.views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^events/', Events.as_view())
]

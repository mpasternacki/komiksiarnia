from django.conf.urls.defaults import *

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^accounts/', include('komiksiarnia.lusers.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'', include('komiksiarnia.komiksy.urls')),
                       )

if settings.DEBUG:
    import os, os.path
    urlpatterns = patterns('',
                           (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
                            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                           ) + urlpatterns

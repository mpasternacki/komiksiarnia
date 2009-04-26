from models import Seria, Pasek
from feeds import KomiksyRSS, KomiksyAtom
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^feed/(?P<url>.*)$','django.contrib.syndication.views.feed', {'feed_dict' : dict(rss=KomiksyRSS,atom=KomiksyAtom)}),
    (r'^$', 'django.views.generic.list_detail.object_list', dict(queryset=Seria.objects.all())))

urlpatterns += patterns('komiksiarnia.komiksy.views',
    (r'^new/$', 'new_redirect'),
    (r'^new/(?P<maxid>\d+)/$', 'new_complex'),
    (r'^(?P<seria>[^/]+)/$', 'seria'),
    (r'^(?P<seria>[^/]+)/random/$', 'random'),
    (r'^(?P<seria>[^/]+)/tag/$', 'tag_list'),
    (r'^(?P<seria>[^/]+)/tag/(?P<tag>[^/]+)/$', 'tag'),
    (r'^(?P<seria>[^/]+)/new/$', 'new_redirect'),
    (r'^(?P<seria>[^/]+)/new/(?P<maxid>\d+)/$', 'new_simple'),
    (r'^(?P<seria>[^/]+)/(?P<namiar>[^/]+)/$', 'pasek'),
    )

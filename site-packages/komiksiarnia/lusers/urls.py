from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
                       (r'^login/$', 'django.contrib.auth.views.login'),
                       (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
                       (r'^passwd/$', 'django.contrib.auth.views.password_change',
                        dict(post_change_redirect='../profile/')),
                       (r'^createuser/$', 'komiksiarnia.lusers.views.createuser'),
                       url(r'^profile/$', 'komiksiarnia.lusers.views.user_profile', name='luser_profile')
                       )

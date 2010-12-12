DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
PROJECT_ROOT = os.path.abspath(os.path.split(__file__)[0])

ADMINS = (
    ('Mailing list', 'komiksy@lists.wafel.com'),
)
SERVER_EMAIL = 'komiksy@marchewa.wafel.com'

MANAGERS = ADMINS

DATABASE_ENGINE='mysql'
DATABASE_NAME='komiksy'
DATABASE_USER='komiksy'
DATABASE_PASSWORD='komiksy'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl-pl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT+'/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/_static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*_rzzvqbpm0-c@%-&3u7myl!_182ik1dudi_8o(jcvr*npn*_4'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'komiksiarnia.urls'

TEMPLATE_DIRS = ( PROJECT_ROOT+"/templates", )

AUTH_PROFILE_MODULE = 'lusers.UserProfile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'tagging',
    'pagination',
    #'django.contrib.sites',
    'komiksiarnia.komiksy',
    'komiksiarnia.lusers',
)

PAGINATION_INVALID_PAGE_RAISES_404 = True

try:
    from local_settings import *        # pyflakes:ignore
except ImportError:
    pass

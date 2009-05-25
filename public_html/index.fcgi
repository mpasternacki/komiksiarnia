#!/usr/bin/python
import sys, os, os.path

root = os.path.realpath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

sys.path.insert(0, os.path.join(root, "site-packages"))
sys.path.insert(1, root)
os.chdir(root)
os.environ['DJANGO_SETTINGS_MODULE'] = "project.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

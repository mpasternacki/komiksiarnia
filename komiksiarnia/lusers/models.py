from django.db import models, connection

from django.contrib import admin
from django.contrib.auth.models import User

from komiksiarnia.komiksy.models import Seria

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    serie_ignorowane = models.ManyToManyField('komiksy.Seria')
    max_id = models.IntegerField()

admin.site.register(UserProfile)

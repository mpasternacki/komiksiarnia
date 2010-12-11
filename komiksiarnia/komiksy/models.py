import re
from collections import defaultdict

from django.db import models, connection
from django.contrib.auth.models import User

import tagging
from tagging.fields import TagField
from tagging.models import Tag

class Seria(models.Model):
    tytul = models.CharField(max_length=192)
    url = models.CharField(max_length=765)
    hard = models.IntegerField(null=True, blank=True)
    kolejnosc = models.IntegerField(null=True, blank=True)
    first = models.OneToOneField('Pasek', db_column='min', related_name='first_of')
    last = models.OneToOneField('Pasek', db_column='max', related_name='last_of')
    fetch_id = models.CharField(max_length=384, blank=True)
    fetch_time = models.DateTimeField()
    fetcher_data = models.CharField(max_length=765, blank=True)
    pelny_tytul = models.CharField(max_length=765, blank=True)

    def __unicode__(self):
        return self.tytul

    def get_absolute_url(self):
        return '/%s/' % self.tytul

    class Meta:
        # managed = False
        db_table = u'serie'
        ordering = ['pelny_tytul']

    def moar(self, maxid):
        return Pasek.objects.filter(id__gt=maxid, seria=self).count()

class Pasek(models.Model):
    seria = models.ForeignKey(Seria, db_column='seria')
    numer = models.IntegerField(unique=True, null=True, blank=True)
    data = models.DateField(unique=True, null=True, blank=True)
    rozszerzenie = models.CharField(unique=True, max_length=255, blank=True)
    plik = models.CharField(max_length=255)
    poprzedni = models.ForeignKey('self', null=True, db_column='poprzedni')
    tytul_paska = models.CharField(max_length=255, blank=True)
    komentarz = models.TextField(blank=True)
    time = models.DateTimeField(null=True, blank=True)
    tagi = TagField()

    class Meta:
        # managed = False
        db_table = u'paski'

    def slug(self):
        rv = None
        if self.numer: rv = str(self.numer)
        else: rv = str(self.data)
        if self.rozszerzenie: rv += ','+self.rozszerzenie
        return rv

    def get_absolute_url(self):
        return "/%s/%s/" % ( self.seria.tytul, self.slug() )

    def naglowek(self):
        rv = ''
        rv += self.seria.pelny_tytul
        if self.numer: rv += ' numer %d' % self.numer
        else: rv += ' %s' % self.data
        if self.rozszerzenie: rv += ', %s' % self.rozszerzenie
        return rv

    def nastepny(self):
        return Pasek.objects.get(poprzedni=self)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def attachments(self):
        return self.attachment_set.all()

    def __unicode__(self):
        return u'%s %s (%d)' % ( self.seria.tytul, self.slug(), self.id )

    @staticmethod
    def max_id():
        cursor = connection.cursor()
        cursor.execute("SELECT max(id) FROM paski;")
        return cursor.fetchone()[0]

tagging.register(Pasek)

class Attachment(models.Model):
    pasek = models.ForeignKey(Pasek, db_column='pasek')
    plik = models.CharField(max_length=255, blank=True, primary_key=True) # hack hack?
    sortorder = models.IntegerField(null=True, blank=True)
    def get_absolute_url(self):
        return 'http://new.komiksiarnia.net/strip/%d,%d' % ( self.pasek.id, self.sortorder )
    class Meta:
        # managed = False
        db_table = u'attachments'
        ordering = ["pasek", "sortorder"]

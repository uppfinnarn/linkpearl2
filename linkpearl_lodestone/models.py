from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from caching.base import CachingManager, CachingMixin

class Race(CachingMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    clan_1 = models.CharField(max_length=50)
    clan_2 = models.CharField(max_length=50, blank=True)
    
    objects = CachingManager()
    
    def __unicode__(self):
        return self.name

class Server(CachingMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    
    objects = CachingManager()
    
    def __unicode__(self):
        return self.name

class GrandCompany(CachingMixin, models.Model):
    class Meta:
        verbose_name_plural = u"grand companies"
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    short = models.CharField(max_length=10)
    
    objects = CachingManager()
    
    def __unicode__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class FreeCompany(models.Model):
    class Meta:
        verbose_name_plural = u"free companies"
    
    lodestone_id = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Character(models.Model):
    GENDER_M = 1
    GENDER_F = 2
    GENDER_CHOICES = [ (GENDER_M, u"Male"), (GENDER_F, u"Female") ]
    
    lodestone_id = models.CharField(max_length=25, unique=True)
    user = models.ForeignKey(User, related_name='characters', blank=True, null=True)
    
    server = models.ForeignKey(Server, related_name='characters')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    title = models.ForeignKey(Title, related_name='characters')
    
    race = models.ForeignKey(Race, related_name='characters', null=True)
    clan = models.IntegerField(choices=[(1, u"First"), (2, u"Second")])
    gender = models.IntegerField(choices=GENDER_CHOICES)
    
    gc = models.ForeignKey(GrandCompany, verbose_name=u"Grand Company", related_name='characters', blank=True, null=True)
    gc_rank = models.IntegerField(u"Grand Company Rank", default=0)
    fc = models.ForeignKey(FreeCompany, verbose_name=u"Free Company", related_name='characters', blank=True, null=True)
    
    def __unicode__(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
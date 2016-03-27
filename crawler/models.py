from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    screen_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    token_secret = models.CharField(max_length=100)
    def __unicode__(self):
        return self.screen_name
    
class Task(models.Model):
    output = models.CharField(max_length=100)         # output filename of archive file
    type = models.CharField(max_length=20)       # (pic, fav, all)
    date = models.DateTimeField(default=timezone.now)   # date of archive file saved
    user = models.ForeignKey(User)                     # mostly token of owner
    message = models.CharField(max_length=50, default='')            # current status (twit id or ...)
    status = models.IntegerField()                     # current status (used for program)
    total = models.IntegerField()                       # total things to be processed
    current = models.IntegerField()                     # currently processed
    def __unicode__(self):
        return self.output

class Log(models.Model):
    task = models.ForeignKey(Task)
    message = models.CharField(max_length=200)
    def __unicode__(self):
        return self.message

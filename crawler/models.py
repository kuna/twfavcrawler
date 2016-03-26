from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    screen_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
class Task(models.Model):
    output = models.CharField(max_length=100, primary_key=True)         # output filename of archive file
    date = models.DateTimeField(default=timezone.now)   # date of archive file saved
    user = models.ForeignKey(User)                     # mostly token of owner
    archivetype = models.CharField(max_length=20)       # (pic, fav, all)
    status = models.CharField(max_length=50)            # current status (twit id or ...)
    total = models.IntegerField()                       # total things to be processed
    current = models.IntegerField()                     # currently processed

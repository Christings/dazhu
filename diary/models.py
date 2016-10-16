from __future__ import unicode_literals
from django.db import models
import tools.webTools as tools
import account
from django.utils import timezone

from django.template.defaultfilters import default

class Diary(models.Model):    
    author = models.ForeignKey(account.models.Account)
    weather = models.CharField(max_length=20)
    body = models.TextField()
   
    timestamp = models.DateField(default=timezone.now)
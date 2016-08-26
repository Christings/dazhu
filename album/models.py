from __future__ import unicode_literals

from django.db import models
import dazhu.settings as settings
import os
import tools.webTools as tools

class Photoes(models.Model):
    rndName = models.CharField(max_length=150)
    showName = models.CharField(max_length=150)
    
    private_choices = (('private', 'private'), ('public', 'public'),)
    phototype = models.CharField('photo_type', choices=private_choices, max_length=10)  
    timestamp = models.DateTimeField()
    def delete(self, using=None):
        try:
            tools.debug("delete file ",settings.BASE_DIR + "/dazhu/static/album/normal/" + self.rndName)
            if os.path.isfile(settings.BASE_DIR + "/dazhu/static/album/normal/" + self.rndName):
                os.remove(settings.BASE_DIR + "/dazhu/static/album/normal/" + self.rndName)
            if os.path.isfile(settings.BASE_DIR + "/dazhu/static/album/mini/" + self.rndName):
                os.remove(settings.BASE_DIR + "/dazhu/static/album/mini/" + self.rndName)
        except Exception as errors:
            tools.debug(errors,"album-models-delete")
        models.Model.delete(self, using=using)
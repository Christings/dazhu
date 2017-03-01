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
        # try:
        normal_path = u"".join([settings.BASE_DIR,"/dazhu/static/album/normal/", self.rndName]).encode("utf-8")
        mini_path = u"".join([settings.BASE_DIR,"/dazhu/static/album/mini/", self.rndName]).encode("utf-8")
        
        tools.debug("delete file ", normal_path)
        if os.path.isfile(normal_path):
            os.remove(normal_path)
        if os.path.isfile(mini_path):
            os.remove(mini_path)
        # except Exception as errors:
        #     tools.debug(errors,"album-models-delete")
        models.Model.delete(self, using=using)
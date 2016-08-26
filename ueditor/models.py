from django.db import models
from blog.models import BlogPost
import os
import dazhu.settings as settings

# Create your models here.
class attachment(models.Model):
    blog = models.ForeignKey(BlogPost)
    sourceName = models.CharField(max_length=150)
    rndName = models.CharField(max_length=150)
    def delete(self, using=None):
        if os.path.isfile(settings.BASE_DIR + "/dazhu/static/upload/" + self.rndName):
            os.remove(settings.BASE_DIR + "/dazhu/static/upload/" + self.rndName)
        models.Model.delete(self, using=using)

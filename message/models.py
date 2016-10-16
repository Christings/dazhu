from __future__ import unicode_literals
import  tools.webTools as tools
from django.db import models

# Create your models here.
class Message(models.Model):
    guid = models.CharField(max_length=15,primary_key=True,blank=True)
    author = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.guid=="":
            self.guid = tools.GetRndStr()

        super(Message, self).save(*args, **kwargs) # Call the "real" save() method.
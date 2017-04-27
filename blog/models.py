from __future__ import unicode_literals
from django.db import models
import tools.webTools as tools
from django.utils import timezone

class BlogPost(models.Model):
    guid = models.CharField(max_length=15,primary_key=True,blank=True)
    author = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    body = models.TextField()
    category = models.CharField(max_length=150)
    timestamp = models.DateTimeField(default = timezone.now)
    last_update = models.DateTimeField(default = timezone.now)
    allow_comment = models.BooleanField(default=True)
    question = models.CharField(max_length=150,default="",blank=True)
    answer = models.CharField(max_length=150,default="",blank=True)
   
    def save(self, *args, **kwargs):
        if self.guid=="":
            self.guid = tools.GetTimeCode()

        if self.guid=="":
            self.guid = tools.GetTimeCode()
        #do_something()
        super(BlogPost, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def delete(self, using=None):
        attachments = self.attachment_set.all()
        for item in attachments:
            item.delete()
        models.Model.delete(self, using=using)
        
class Category(models.Model):
    title = models.CharField(max_length=150)
    is_privite = models.BooleanField(default=False)
    
class Comment(models.Model):
    blog = models.ForeignKey(BlogPost)
    author = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField(default = timezone.now)
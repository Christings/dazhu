from django.db import models
from blog.models import BlogPost
import os
import dazhu.settings as settings

# Create your models here.
class CmsItem(models.Model):
    title = models.CharField(max_length=150)
    contentData = models.TextField()
    controller = models.CharField(max_length=150)
    view = models.CharField(max_length=150)
    itemID = models.IntegerField(default=0)

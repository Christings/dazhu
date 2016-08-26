from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from account.models import Account
# Create your models here.
class Memo(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Account)
    body = models.TextField()
    timestamp = models.DateTimeField(default = timezone.now)
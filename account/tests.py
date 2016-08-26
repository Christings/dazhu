from django.test import TestCase
from models import Account

# Create your tests here.
class TestCase1(TestCase):
    def setUp(self):
        account = Account()
        account.username ="yzh"
        account.userpwd ="yzh"
        account.is_active = True
        account.save()

      
from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User

# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, unique = True)

class Stock(models.Model):
    stock_tickr = models.CharField(max_length = 5, null = False, blank = False)
    stock_name = models.CharField(max_length = 50, null = False, blank = False)
    users = models.ManyToManyField(User)
    
    def __unicode__(self):
        return smart_unicode(self.stock_name) # For accented character conversion
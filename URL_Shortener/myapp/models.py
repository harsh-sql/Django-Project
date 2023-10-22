from django.db import models

# Create your models here.
class LongToShort(models.Model):
	long_url=models.URLField(max_length=500)
	short_url=models.CharField(max_length=50, unique=True)
	date=models.DateField(auto_now_add=True)
	clicks=models.IntegerField(default=0)
	mobile_visits=models.IntegerField(default=0)
	desktop_visits=models.IntegerField(default=0)

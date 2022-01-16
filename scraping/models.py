from django.db import models


class Announce(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    city = models.CharField(max_length=255)
    date = models.DateTimeField('date')
    type = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True)
    source = models.CharField(max_length=255)
    original_date = models.CharField(max_length=255)
    original_time = models.CharField(max_length=255)


from django.db import models


class Type(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)


class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)


class Announce(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    city = models.CharField(max_length=255)
    date = models.DateTimeField('date')
    type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    original_date = models.CharField(max_length=255)
    original_time = models.CharField(max_length=255)
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    # type = models.ForeignKey(Type, on_delete=models.CASCADE)


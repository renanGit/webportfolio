"""
Example model to test graphql
"""

from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=50)


class CountryOrigin(models.Model):
    country = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)
    country_origin = models.ForeignKey(CountryOrigin, on_delete=models.CASCADE)
    year = models.IntegerField()

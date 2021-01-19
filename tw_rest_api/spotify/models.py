from django.db import models
from datetime import datetime


class Album(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now)


class Song(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField()
    views = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)

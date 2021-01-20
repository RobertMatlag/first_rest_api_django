from django.db import models
from datetime import datetime


class Album(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField()
    views = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name

    # def values(self):
    #     data = {
    #         "name": self.name,
    #         "songs": self.author,
    #         "pictures": list(Picture.objects.filter(game__pk=self.id).values('url')),
    #         "urls": list(Url.objects.filter(game__pk=self.id).values('adress')),
    #     }
    #
    # return data

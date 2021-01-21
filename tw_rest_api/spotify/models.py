from django.db import models
from datetime import datetime
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE, SOFT_DELETE_CASCADE


class Album(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Song(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    name = models.CharField(max_length=200)
    length = models.IntegerField()
    views = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Playlist(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name

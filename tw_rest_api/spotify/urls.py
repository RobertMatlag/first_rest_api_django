from django.urls import path

from .views import album_view, song_view, playlist_view

urlpatterns = [
    path('albums/', album_view.AlbumView.as_view()),
    path('albums/<int:pk>/', album_view.AlbumView.as_view()),
    path('songs/', song_view.SongView.as_view()),
    path('songs/<int:pk>/', song_view.SongView.as_view()),
    path('playlists/', playlist_view.PlaylistView.as_view()),
    path('playlists/<int:pk>/', playlist_view.PlaylistView.as_view()),
]

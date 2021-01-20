from django.urls import path

from .views import AlbumView, SongView, PlaylistView

urlpatterns = [
    path('albums/', AlbumView.as_view()),
    path('albums/<int:pk>/', AlbumView.as_view()),
    path('songs/', SongView.as_view()),
    path('songs/<int:pk>/', SongView.as_view()),
    path('playlists/', PlaylistView.as_view()),
    path('playlists/<int:pk>/', PlaylistView.as_view()),
]

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from ..models import Song, Playlist
from ..views import delete_record, handle_get_request


class PlaylistView(View):
    @staticmethod
    def get(request, pk=None):
        return handle_get_request(pk, Playlist, request)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PlaylistView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            new_playlist = Playlist(name=data.get('name'))
            new_playlist.save()
            PlaylistView._add_songs_to_playlist(new_playlist, data.get('songs'))
            return JsonResponse({"created": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not valid data"}, safe=False)

    def patch(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            playlist = Playlist.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "name":
                    playlist.name = data[key]
                if key == "songs":
                    playlist.songs.clear()
                    PlaylistView._add_songs_to_playlist(playlist, data.get('songs'))
            playlist.save()
            return JsonResponse({"updated": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Playlist.DoesNotExist:
            return JsonResponse({"error": "Your playlist having provided primary key does not exist"}, safe=False)

    def put(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            playlist = Playlist.objects.get(pk=pk)
            playlist.name = data['name']
            playlist.songs.clear()
            PlaylistView._add_songs_to_playlist(playlist, data.get('songs'))
            playlist.save()
            return JsonResponse({"overwrite": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Playlist.DoesNotExist:
            return JsonResponse({"error": "Your playlist having provided primary key does not exist"}, safe=False)

    @staticmethod
    def delete(request, pk):
        return delete_record(Playlist, pk)

    @staticmethod
    def _add_songs_to_playlist(playlist, songs_id):
        for song_id in songs_id:
            song = Song.objects.get(pk=song_id)
            playlist.songs.add(song)

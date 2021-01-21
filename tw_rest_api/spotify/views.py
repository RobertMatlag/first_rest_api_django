from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.core.serializers import serialize


from .models import Album, Song, Playlist


def _send_chosen_page(request, records):
    page = int(request.GET.get('page', '1'))
    records_per_page = 10
    start_record = (page - 1) * records_per_page
    last_record = start_record + records_per_page
    return JsonResponse(records[start_record:last_record], safe=False)


def _send_one_record(class_name, pk):
    try:
        album = class_name.objects.filter(pk=pk)
        data = serialize("json", album, fields=('name', 'pub_date'))
        return HttpResponse(data, content_type="application/json")
    except json.JSONDecodeError:
        return JsonResponse({"error": "not valid data"}, safe=False)
    except class_name.DoesNotExist:
        return JsonResponse({"error": "Your record having provided primary key does not exist"}, safe=False)


def delete_record(class_name, pk):
    try:
        obj = class_name.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({"deleted": True}, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({"error": "not a valid primary key"}, safe=False)


def _handle_get_request(pk, class_name, request):
    if not pk:
        objs = list(class_name.objects.values())
        return _send_chosen_page(request, objs)
    return _send_one_record(class_name, pk)


class AlbumView(View):
    @staticmethod
    def get(request, pk=None):
        return _handle_get_request(pk, Album, request)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            new_album = Album(name=data.get('name'))
            new_album.save()

            return JsonResponse({"created": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not valid data"}, safe=False)

    def patch(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            album = Album.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "name":
                    album.name = data[key]
                if key == "pub_date":
                    album.pub_date = data[key]
            album.save()
            return JsonResponse({"updated": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Album.DoesNotExist:
            return JsonResponse({"error": "Your album having provided primary key does not exist"}, safe=False)

    def put(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            album = Album.objects.get(pk=pk)

            album.name = data['name']
            album.pub_date = data['pub_date']
            album.save()
            return JsonResponse({"overwrite": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Album.DoesNotExist:
            return JsonResponse({"error": "Your album having provided primary key does not exist"}, safe=False)

    @staticmethod
    def delete(request, pk):
        return delete_record(Album, pk)


class SongView(View):
    @staticmethod
    def get(request, pk=None):
        return _handle_get_request(pk, Song, request)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SongView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            new_song = Song(name=data.get('name'), length=data.get('length'), views=data.get('views'),
                            album=Album.objects.get(pk=data.get('album')))
            new_song.save()

            return JsonResponse({"created": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not valid data"}, safe=False)

    def patch(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            song = Song.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "name":
                    song.name = data[key]
                if key == "length":
                    song.length = data[key]
                if key == "views":
                    song.views = data[key]
                if key == "album":
                    song.album = Album(pk=data[key])
            song.save()
            return JsonResponse({"updated": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Your song having provided primary key does not exist"}, safe=False)

    def put(self, request, pk):
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
            song = Song.objects.get(pk=pk)

            song.name = data['name']
            song.length = data['length']
            song.views = data['views']
            song.album = Album(pk=data['album'])
            song.save()
            return JsonResponse({"overwrite": data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "not a valid data"}, safe=False)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Your song having provided primary key does not exist"}, safe=False)

    @staticmethod
    def delete(request, pk):
        return delete_record(Song, pk)


class PlaylistView(View):
    @staticmethod
    def get(request, pk=None):
        return _handle_get_request(pk, Playlist, request)

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

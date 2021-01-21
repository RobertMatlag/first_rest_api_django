from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from ..models import Album, Song
from ..views import delete_record, handle_get_request


class SongView(View):
    @staticmethod
    def get(request, pk=None):
        return handle_get_request(pk, Song, request)

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

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from ..models import Album
from ..views import delete_record, handle_get_request


class AlbumView(View):
    @staticmethod
    def get(request, pk=None):
        return handle_get_request(pk, Album, request)

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

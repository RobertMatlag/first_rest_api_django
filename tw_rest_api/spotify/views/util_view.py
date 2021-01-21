from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse
import json


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


def handle_get_request(pk, class_name, request):
    if not pk:
        objs = list(class_name.objects.values())
        return _send_chosen_page(request, objs)
    return _send_one_record(class_name, pk)

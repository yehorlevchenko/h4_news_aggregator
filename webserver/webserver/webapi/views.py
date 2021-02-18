from django.http import JsonResponse
from django.core import serializers
from copy import copy
import json
from webserver.webapi.models import News, Tags, NewsToTags, TgUser


def start(request):
    if request.method == 'GET':
        user, _ = TgUser.objects.get_or_create(id=int(request.GET['id']))
        user.username = request.GET.get('username')
        user.first_name = request.GET.get('first_name')
        user.last_name = request.GET.get('last_name')
        user.language_code = request.GET.get('language_code')
        user.save()
        return JsonResponse({'status_code': 200})


def news(request):
    if request.method == 'GET':
        # TODO: MAJOR FIX: unknown parameters cause objects.all(), should return 403 Bad Request
        field_names = [field.name for field in News._meta.get_fields()]
        valid_parameters = [parameter for parameter in request.GET if parameter in field_names]
        kwargs = {par: request.GET[par] for par in valid_parameters}
        try:
            news_list = News.objects.filter(**kwargs)
        except Exception as e:
            return JsonResponse({'status_code': 500,
                                 'response': [],
                                 'error': e})
        if news_list:
            news_list = _serialize_to_json(news_list)
            return JsonResponse({'status_code': 200,
                                 'response': news_list,
                                 'error': None})
        else:
            return JsonResponse({'status_code': 404,
                                 'response': [],
                                 'error': None})


def _serialize_to_json(data):
    """
    Will get a queryset, serialize it to JSON in a format:
    [{"id": pk, "%model_field_1%": "%model_value_1%", [...]}]
    :param data:
    :return:
    """
    raw_data = json.loads(serializers.serialize('json', data))
    result = []
    for item in raw_data:
        item_dict = {'id': item['pk']}
        item_dict.update(item['fields'])
        result.append(item_dict)
    # return json.dumps(result, skipkeys=True, ensure_ascii=False)
    return result


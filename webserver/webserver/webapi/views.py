from django.http import JsonResponse
from django.core import serializers
import json
from webserver.webapi.models import News, Tags, NewsToTags


def news(request):
    FILTERING_FIELDS = ('source_api', 'title', 'abstract',
                        'slug_name', 'published_date')

    if request.method == 'GET':
        if 'id' in request.GET:
            id = int(request.GET['id'])
            news = [News.objects.get(pk=id)]
        else:
            get_parameters = request.GET.items()
            filter = {key: value for (key, value) in get_parameters
                      if key in FILTERING_FIELDS}
            news = News.objects.filter(**filter)

        # TODO: use _serialize_to_json(news)
        news = _serialize_to_json(news)
        return JsonResponse({'response': news})

    #     # TODO: use _serialize_to_json(news)
    #     news = _serialize_to_json(news)
    #     return JsonResponse({'response': news})


def _serialize_to_json(data):
    """
    Will get a queryset, serialize it to JSON in a format:
    [{"id": pk, "%model_field_1%": "%model_value_1%", [...]}]
    :param data:
    :return:
    """
    raw_data = json.loads(serializers.serialize('json', data))
    # TODO: add dicts reformatting
    return raw_data


from django.http import JsonResponse
from django.core import serializers
import json
from webserver.webapi.models import News, Tags, NewsToTags


def news(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            id = int(request.GET['id'])
            news = [News.objects.get(pk=id)]
        else:
            objects_req_name = ['source_api', 'published_date']
            objects = [item for item in request.GET if item in objects_req_name]
            for items in objects_req_name:
                if items in request.GET:
                    news = News.objects.filter(objects[items])
                else:
                    news = News.objects.all()
        news = _serialize_to_json(news)
        return JsonResponse({'response': news})


def _serialize_to_json(data):
    """
    Will get a queryset, serialize it to JSON in a format:
    [{"id": pk, "%model_field_1%": "%model_value_1%", [...]}]
    :param data:
    :return:
    """
    raw_data = json.loads(serializers.serialize('json', data))
    # TODO: add dicts reformatting
    output = list()
    input = dict()
    for key, item in raw_data.items():
        input = {'id': item['pk']}
        if 'fields' in key:
            input.update(item[key])
        output.append(input)
    return json.dumps(output)



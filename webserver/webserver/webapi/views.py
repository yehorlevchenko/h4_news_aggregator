from django.http import JsonResponse
from django.core import serializers
import json
from webserver.webapi.models import News, Tags, NewsToTags


def news(request):
    news = News.objects.all()
    if 'source_api' in request.GET:
        news = news.filter(source_api=request.GET['source_api'])
    news = json.loads(serializers.serialize('json', news))
    return JsonResponse({'response': news})

from rest_framework import viewsets
from webserver.webapi.serializers import NewsSerializer, TagsSerializer, NewsToTagsSerializer
from webserver.webapi.models import News, Tags, NewsToTags


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class TagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class NewsToTagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NewsToTags.objects.all()
    serializer_class = NewsToTagsSerializer

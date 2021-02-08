from rest_framework import serializers

from webserver.webapi.models import News, Tags, NewsToTags


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['published_date', 'title', 'abstract', 'url', 'media_url',
                  'source_api']


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['source_api', 'tag_name', 'tag_group']



class NewsToTagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsToTags
        fields = ['news_id', 'tag_id']


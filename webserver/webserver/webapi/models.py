from django.db import models


class News(models.Model):
    id = models.AutoField(primary_key=True)
    source_api = models.CharField(max_length=50)
    title = models.CharField(max_length=512)
    abstract = models.TextField(blank=True, null=True)
    slug_name = models.CharField(max_length=128)
    published_date = models.DateTimeField()
    url = models.TextField()
    internal_source = models.CharField(max_length=256, blank=True, null=True)
    media_url = models.TextField(blank=True, null=True)
    media_copyright = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'
        unique_together = (('source_api', 'slug_name', 'published_date'),)


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    source_api = models.CharField(max_length=50)
    tag_name = models.CharField(max_length=256)
    tag_group = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'
        unique_together = (('source_api', 'tag_name', 'tag_group'),)


class NewsToTags(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(News, on_delete=models.DO_NOTHING, db_column='news_id')
    tag_id = models.ForeignKey(Tags, on_delete=models.DO_NOTHING, db_column='tag_id')

    class Meta:
        managed = False
        db_table = 'news_to_tags'


class TgUser(models.Model):
    username = models.CharField(max_length=1024, null=True)
    first_name = models.CharField(max_length=1024, blank=True, null=True)
    second_name = models.CharField(max_length=1024, blank=True, null=True)
    language_code = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tg_user'


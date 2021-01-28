from django.db import models

# Create your models here.


class News(models.Model):
    source_api = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=512, null=False)
    abstract = models.TextField(null=False)
    slug_name = models.CharField(max_length=128, null=False)
    published_date = models.DateTimeField(auto_now=False, null=False)
    url = models.TextField(null=False)
    internal_source = models.CharField(max_length=128)
    media_url = models.CharField(max_length=1024)
    media_copyright = models.CharField(max_length=256)



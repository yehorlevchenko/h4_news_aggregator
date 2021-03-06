# Generated by Django 3.0.7 on 2021-02-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source_api', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=512)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('slug_name', models.CharField(max_length=128)),
                ('published_date', models.DateTimeField()),
                ('url', models.TextField()),
                ('internal_source', models.CharField(blank=True, max_length=256, null=True)),
                ('media_url', models.TextField(blank=True, null=True)),
                ('media_copyright', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'news',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NewsToTags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'news_to_tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source_api', models.CharField(max_length=50)),
                ('tag_name', models.CharField(max_length=256)),
                ('tag_group', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
        ),
    ]

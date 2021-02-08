from django.urls import include, path
from rest_framework import routers
from webserver.webapi import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'tags', views.TagsViewSet)
router.register(r'news_to_tags', views.NewsToTagsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

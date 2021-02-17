from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('api/', include('webserver.webapi.urls')),
    path('admin/', admin.site.urls),
]

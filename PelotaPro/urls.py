from django.contrib import admin
from django.urls import path, include,re_path

from django.conf import settings
from django.conf.urls.static import static


from django.views.static import serve

static_urlpatterns = [
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    path("", include("main.urls")),
    path('admin/', admin.site.urls),
    path("", include(static_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
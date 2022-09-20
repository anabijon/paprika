from cgitb import handler
from importlib.metadata import PackageNotFoundError
from os import stat
from pydoc import pager
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/piza/', include('piza.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, Document_root=settings.MEDIA_ROOT)
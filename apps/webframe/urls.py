from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^images$', views.image),
    url(r'^live$', views.webcam),
    url(r'^upload$', views.upload),
    url(r'^ml_image$', views.ml_image),
    url(r'^ml_process$', views.ml_process),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
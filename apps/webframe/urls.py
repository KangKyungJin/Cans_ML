from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^images$', views.image),
    url(r'^live$', views.webcam),
    url(r'^upload$', views.upload),
]
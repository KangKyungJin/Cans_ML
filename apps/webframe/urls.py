from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^images$', views.images),
    url(r'^live$', views.webcam)
]
from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^search', views.search),
    url(r'^profile', views.profile),
    url(r'^', views.hello),
]

import os
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
]

if settings.DEBUG:
    urlpatterns += path('error=404', views.handle404),
    urlpatterns += path('error=500', views.handle500),

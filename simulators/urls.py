from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nibp', views.nibp, name='nibp'),
    path('ecg', views.ecg, name='ecg'),
    path('spo2', views.spo2, name='spo2'),
    path('sim_abiertos', views.sim_abiertos, name='sim_abiertos'),
    path('videos', views.videos, name='videos'),
    path('links', views.links, name='links'),
]

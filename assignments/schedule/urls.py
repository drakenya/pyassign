from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.by_date, name='index'),
    url('^date', views.by_date, name='by_date'),
    url('^name', views.by_name, name='by_name'),
    url('^incoming$', views.incoming, name='incoming_speakers'),
]
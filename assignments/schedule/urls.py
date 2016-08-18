from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.by_date, name='index'),
    url('^date', views.by_date, name='by_date'),
    url('^name', views.by_name, name='by_name'),
    url('^incoming$', views.incoming, name='incoming_speakers'),
    url('^outgoing$', views.outgoing, name='outgoing_speakers'),
    url('^sound$', views.sound, name='sound_schedule'),
    url('^chairman-reader$', views.chairman_reader, name='chairman_reader_schedule'),
    url('^todays-emails$', views.todays_emails, name='todays_emails'),
]
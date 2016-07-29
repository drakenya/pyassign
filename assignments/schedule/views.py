from django.shortcuts import render
from django.db import connection
from django.contrib.auth.models import User

from .models import Assignment, Incoming, Part, Account


# Create your views here.
def index(request):
    context = {}
    return render(request, 'schedule/index.html', context)


def by_date(request):
    assignments = Assignment.objects.order_by('date')
    context = {'assignments': assignments}
    return render(request, 'schedule/date.html', context)


def by_name(request):
    assignments = Assignment.objects.order_by('account__user__last_name', 'account__user__first_name')
    context = {'assignments': assignments}
    return render(request, 'schedule/name.html', context)


def incoming(request):
    sql = """
        SELECT {0}.date, speaker_full_name, congregation_name, outline_name, first_name, last_name
        FROM {0}
            LEFT JOIN {1} ON ({0}.date = {1}.date)
            LEFT JOIN {2} ON ({2}.id = {1}.part_id)
            LEFT JOIN {3} ON ({3}.id = {1}.account_id)
            LEFT JOIN {4} ON ({4}.id = {3}.user_id)
        WHERE ({2}.short_name = 'h' OR {2}.id IS NULL)
        """.format(Incoming._meta.db_table, Assignment._meta.db_table, Part._meta.db_table, Account._meta.db_table, User._meta.db_table)
    cursor = connection.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    incoming_speakers = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {'incoming_speakers': incoming_speakers}
    return render(request, 'schedule/incoming.html', context)


def outgoing(request):
    outging_speakers = Assignment.objects.filter(part__short_name='pt').order_by('date')
    context = {'outgoing_speakers': outging_speakers}
    return render(request, 'schedule/outgoing.html', context)


def sound(request):
    all_sound = Assignment.objects.filter(part__short_name__in=['console', 'rove1', 'rove2', 'stage', 'att'])
    sound_schedule = {}

    for item in all_sound:
        if not str(item.date) in sound_schedule:
            sound_schedule[str(item.date)] = {'date': item.date}

        sound_schedule[str(item.date)][item.part.short_name] = item

    context = {'sound_schedule': sound_schedule}
    return render(request, 'schedule/sound.html', context)

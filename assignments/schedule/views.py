from datetime import date

from django.shortcuts import redirect, render
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Assignment, Incoming, Part, Account
from .management.email import emailing
from .management.loaders.controller import LoadController


# Create your views here.
@login_required
def index(request):
    context = {}
    return render(request, 'schedule/index.html', context)


@login_required
def by_date(request):
    assignments = Assignment.objects.filter(date__gte=date.today()).order_by('date')
    context = {'assignments': assignments}
    return render(request, 'schedule/date.html', context)


@login_required
def by_name(request):
    assignments = Assignment.objects.filter(date__gte=date.today()).order_by('account__user__last_name', 'account__user__first_name')
    context = {'assignments': assignments}
    return render(request, 'schedule/name.html', context)


@login_required()
def my_assignments(request):
    assignments = Assignment.objects.filter(date__gte=date.today()).filter(account__user__id=request.user.id).order_by('account__user__last_name', 'account__user__first_name')
    context = {'assignments': assignments}
    return render(request, 'schedule/name.html', context)


@login_required()
def incoming(request):
    sql = """
        SELECT {0}.date, speaker_full_name, congregation_name, outline_name, first_name, last_name
        FROM {0}
            LEFT JOIN {1} ON ({0}.date = {1}.date)
            LEFT JOIN {2} ON ({2}.id = {1}.part_id)
            LEFT JOIN {3} ON ({3}.id = {1}.account_id)
            LEFT JOIN {4} ON ({4}.id = {3}.user_id)
        WHERE {0}.date >= '{5}'
            AND ({2}.short_name = 'h' OR {2}.id IS NULL)
        """.format(Incoming._meta.db_table,   # {0}
                   Assignment._meta.db_table, # {1}
                   Part._meta.db_table,       # {2}
                   Account._meta.db_table,    # {3}
                   User._meta.db_table,       # {4}
                   date.today()               # {5}
                  )
    cursor = connection.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    incoming_speakers = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {'incoming_speakers': incoming_speakers}
    return render(request, 'schedule/incoming.html', context)


@login_required()
def outgoing(request):
    outging_speakers = Assignment.objects.filter(date__gte=date.today()).filter(part__short_name='pt').order_by('date')
    context = {'outgoing_speakers': outging_speakers}
    return render(request, 'schedule/outgoing.html', context)


@login_required()
def sound(request):
    all_sound = Assignment.objects.filter(date__gte=date.today()).filter(part__short_name__in=['console', 'rove1', 'rove2', 'stage', 'att'])
    sound_schedule = {}

    for item in all_sound:
        if not str(item.date) in sound_schedule:
            sound_schedule[str(item.date)] = {'date': item.date}

        sound_schedule[str(item.date)][item.part.short_name] = item

    context = {'sound_schedule': sound_schedule}
    return render(request, 'schedule/sound.html', context)


@login_required()
def chairman_reader(request):
    all_chairman_reader = Assignment.objects.filter(date__gte=date.today()).filter(part__short_name__in=['chr', 'wtr'])
    chairman_reader_schedule = {}

    for item in all_chairman_reader:
        if not str(item.date) in chairman_reader_schedule:
            chairman_reader_schedule[str(item.date)] = {'date': item.date}

        chairman_reader_schedule[str(item.date)][item.part.short_name] = item

    context = {'chairman_reader_schedule': chairman_reader_schedule}
    return render(request, 'schedule/chairman_reader.html', context)


@user_passes_test(lambda u: u.is_superuser)
def todays_emails(request):
    emailings = emailing.Email.get_todays_emails()
    context = {'emailings': emailings}
    return render(request, 'schedule/todays_emails.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_all(request):
    LoadController.load_all()
    return redirect('index')
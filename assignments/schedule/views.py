from django.shortcuts import render

from .models import Assignment


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

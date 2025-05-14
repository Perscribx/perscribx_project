from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from notifications.models import Summary, Task


# Create your views here.
class SummaryListView(ListView):
    queryset = Summary.objects.all()
    context_object_name = 'summaries'
    paginate_by = 5
    template_name = 'notifications/list.html'

@login_required
def summary_list(request):
    object_list = Summary.objects.all()


    paginator = Paginator(object_list, 5)  # 10
    page = request.GET.get('page')
    try:
        summaries = paginator.page(page)
    except PageNotAnInteger:
        summaries = paginator.page(1)
    except EmptyPage:
        summaries = paginator.page(paginator.num_pages)
    return render(request,
                  'notifications/list.html',
                  {'page': page,
                   'summaries': summaries})

@login_required
def summary_detail(request, year, month, day, slug):
    summary = get_object_or_404(Summary, slug=slug,
                                date__year=year,
                                date__month=month,
                                date__day=day)
    tasks = Task.objects.get_queryset().filter(summary__slug=slug)
    return render(request,
                  'notifications/detail.html',
                  {'summary': summary,
                   'tasks': tasks})

@login_required
def task_detail(request, year, month, day, slug, task_slug):
    task = get_object_or_404(Task, summary__date__year=year, summary__date__month=month, summary__date__day=day,
                             summary__slug=slug, slug=task_slug)
    return render(request,
                  'tasks/detail.html',
                  {'task': task})

@login_required
def task_list(request):
    object_list = Task.objects.all().order_by('-summary__priority', 'date')

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request,
                  'tasks/list.html',
                  {'page': page,
                   'tasks': tasks})

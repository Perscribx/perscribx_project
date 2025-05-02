from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from notifications.models import Summary


# Create your views here.
class SummaryListView(ListView):
    queryset = Summary.objects.all()
    context_object_name = 'summaries'
    paginate_by = 20
    template_name = 'notifications/list.html'


def summary_detail(request, year, month, day, slug):
    summary = get_object_or_404(Summary, slug=slug,
                                date__year=year,
                                date__month=month,
                                date__day=day)

    return render(request,
                  'notifications/detail.html',
                  {'summary': summary,})
from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.SummaryListView.as_view(), name='summary_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.summary_detail, name='summary_detail')
]
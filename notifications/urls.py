from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.summary_list, name='summary_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.summary_detail, name='summary_detail'),
    path('tasks', views.task_list, name='task_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/<slug:task_slug>', views.task_detail, name='task_detail')
]
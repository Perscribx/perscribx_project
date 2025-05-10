from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.summary_list, name='summary_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.summary_detail, name='summary_detail')
]
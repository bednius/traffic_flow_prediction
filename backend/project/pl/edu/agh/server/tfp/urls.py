from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trigger', views.trigger, name='trigger'),
    path('results/<int:result_id>/', views.results, name='results')
]
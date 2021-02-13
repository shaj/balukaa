
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('a', views.about, name='about'),
    path('newtask', views.create_task, name='create_task'),
]

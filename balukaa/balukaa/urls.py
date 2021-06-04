"""balukaa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .nav_main_list import MENU

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    path('',
         TemplateView.as_view(
             template_name="home.html",
             extra_context={
                 'title': 'Главная',
                 'menu_list': MENU,
             }),
         name='home'
         ),
    path('about/',
         TemplateView.as_view(
             template_name="about.html",
             extra_context={
                 "title": "О нас",
                 'menu_list': MENU,
             }),
         name='about'
         ),

    path('', include('todo.urls', namespace='todo')),
    path('', include('registration.urls', namespace='registration')),
    path('ledger/', include('ledger.urls', namespace='ledger')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

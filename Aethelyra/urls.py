"""Aethelyra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, static
from django.contrib import admin
from rpgroup5 import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from .settings import STATIC_URL

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage),
    url(r'^chapters/$', views.chapters_admin),
    url(r'^chapters/add/$', views.new_chapter),
    url(r'^chapters/edit/$', views.edit_chapter),
    url(r'^chapters/(?P<action>.+)/success/$', views.success),
    url(r'^view/$', views.view_chapter),
    url(r'^login/$', auth_views.login, {'template_name': 'rpgroup5/registration/login.html'}, name='login'),
    url(r'^chatlogs/admin/add/$', views.new_chatlog),
    url(r'^chatlogs/admin/(?P<group>\w+)/(?P<action>\w+)/success/$', views.chatlog_success),
    url(r'^chatlogs/admin/(?P<group>\w+)/edit/$', views.chatlog_edit),
    url(r'^chatlogs/admin/$', views.chatlog_admin),
    url(r'^chatlogs/admin/(?P<action>.+)/success/(?P<group>.*)$', views.chatlog_success),
    url(r'^chatlogs/(?P<group>\w+)/$', views.chatlog_view),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""devops URL Configuration

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
from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^ci_category/$', views.CategoryListView, name='CategoryList'),
    url(r'^ci_category/listAPI', views.CategoryListViewAPI, name='CategoryListAPI'),
    url(r'^ci_category/create/$', views.CategoryCreateView, name='CategoryCreate'),
    url(r'^ci_category/(?P<pk>\d+)/detail/$', views.CategoryDetailView, name='CategoryDetail'),
    url(r'^ci_category/(?P<pk>\d+)/update/$', views.CategoryUpdateView, name='CategoryUpdate'),
    url(r'^ci_category/(?P<pk>\d+)/delete/$', views.CategoryDeleteView, name='CategoryDelete'),
    url(r'^ci_property/(?P<pk>\d+)/update/$', views.PropertyUpdateView, name='PropertyUpdate'),
    url(r'^ci_property/(?P<category_pk>\d+)/add/$', views.PropertyCreateView, name='PropertyCreate'),
    url(r'^ci_property/(?P<pk>\d+)/delete/$', views.PropertyDeleteView, name='PropertyDelete'),
    url(r'^host/$', views.HostListView, name='HostList'),
    url(r'^host/listAPI/', views.HostListViewAPI, name='HostListAPI'),
    url(r'^host/createOrUpdate/$', views.CreateOrUpdateHostAPI, name='CreateOrUpdateHost'),
    url(r'^host/setTable/$', views.setTable, name='setTable'),
    url(r'^host/detail/(?P<server_id>.+)/$', views.HostDetailView, name='HostDetail'),
    url(r'^host/update/(?P<server_id>.+)/$', views.HostUpdateView, name='HostUpdate'),
    url(r'^host/delete/(?P<server_id>.+)/$', views.HostDeleteView, name='HostDelete'),
    url(r'^host/zabbix/(?P<ip>.+)/$', views.zabbix, name='zabbix'),
    url(r'^host/zabbix_refresh/$', views.zabbix_refresh, name='zabbix_refresh'),
    url(r'^host/add/$', views.HostAddView, name='HostAdd'),
]
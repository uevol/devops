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

urlpatterns = [
    url(r'^cmd/', views.RemoteCmdView, name="RemoteCmd"),
    url(r'^select_host/', views.SelectHostView, name="SelectHost"),
    url(r'^job_list/$', views.JobListView, name="JobList"),
    url(r'^job_list/api/$', views.JobListViewAPI, name="JobListAPI"),
    url(r'^job_list/detail/(?P<cjid>.+)/$', views.JobResultView, name="JobResult"),
    url(r'^file/$', views.PushFileVifew, name="PushFile"),
    url(r'^file/upload/$', views.UploadFileVifew, name="UploadFile"),
    url(r'^file/delete/(?P<pk>\d+)/$', views.FileDeleteView, name="FileDelete"),
    url(r'^script/$', views.ScriptListView, name="ScriptList"),
    url(r'^script/listAPI/', views.ScriptListViewAPI, name="ScriptListAPI"),
    url(r'^script/edit/(?P<pk>\d+)/$', views.ScriptEditView, name="ScriptEdit"),
    url(r'^script/run/(?P<pk>\d+)/$', views.ScriptRunView, name="ScriptRun"),
    url(r'^state/$', views.StateListView, name="StateList"),
    url(r'^state/listAPI/', views.StateListViewAPI, name="StateListView"),
    url(r'^state/run/(?P<pk>\d+)/$', views.StateRunView, name="StateRun"),
]
"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', views.include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/$', views.UserListView, name='UserList'),
    url(r'^user/list/', views.UserListAPI, name='UserListAPI'),
    url(r'^user/create/', views.UserCreateView, name='UserCreate'),
    url(r'^user/(?P<pk>\d+)/update', views.UserUpdateView, name='UserUpdate'),
    url(r'^user/(?P<pk>\d+)/detail', views.UserDetailView, name='UserDetail'),
    url(r'^user/(?P<pk>\d+)/resetpassword', views.UserResetPdView, name='UserResetPd'),
    url(r'^user/(?P<pk>\d+)/changepassword', views.UserChangePdView, name='UserChangePd'),
    url(r'^user/(?P<pk>\d+)/delete', views.UserDeleteView, name='UserDelete'),
    url(r'^group/$', views.GroupListView, name='GroupList'),
    url(r'^group/search/', views.GroupSearchView, name='GroupSearch'),
    url(r'^group/create/', views.GroupCreateView, name='GroupCreate'),
    url(r'^group/(?P<gid>\d+)/delete_user/(?P<uid>\d+)/', views.DeleteUserFromGroup, name='DeleteUserFromGroup'),
    url(r'^group/(?P<pk>\d+)/update', views.GroupUpdateView, name='GroupUpdate'),
    url(r'^group/(?P<pk>\d+)/delete/$', views.GroupDeleteView, name='GroupDelete'),
    url(r'^role/$', views.RoleListView, name='RoleList'),
    url(r'^role/create/', views.RoleCreateView, name='RoleCreate'),
    url(r'^role/search/', views.RoleSearchView, name='RoleSearch'),
    url(r'^role/(?P<rid>\d+)/delete_user/(?P<uid>\d+)/', views.DeleteUserFromRole, name='DeleteUserFromRole'),
    url(r'^role/(?P<pk>\d+)/update', views.RoleUpdateView, name='RoleUpdate'),
    url(r'^role/(?P<pk>\d+)/delete/$', views.RoleDeleteView, name='RoleDelete'),
    url(r'^permission/update/$', views.PermUpdateView, name='PermUpdate'),
    url(r'^permission/', views.PermListView, name='PermList'),
    url(r'^service/$', views.ServiceListView, name='ServiceList'),
    url(r'^service/(?P<pk>\d+)/update/$', views.ServiceUpdateView, name='ServiceUpdate'),
]
# coding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from cmdb.models import CiCategory
from admins.models import Service

def login(request):
    """ user login """
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'The acount is not actived or not exsit.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'The username or password is incorrect .')
            return render(request, 'login.html')

@login_required
def logout(request):
    """ user logout """
    auth_logout(request)
    messages.info(request, 'Logout successfully !')
    return render(request, 'login.html')

class BaseView(TemplateView):
    ''' base view '''
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['CiCategory'] = CiCategory.objects.filter(show_in_left=True)
        context['webssh'] = Service.objects.get(name='webssh')
        return context

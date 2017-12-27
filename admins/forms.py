# coding=utf-8
from django import forms
from .models import Role

class UserForm(forms.Form):
    ''' user form '''
    username = forms.CharField(max_length=100, label='用户名')
    email = forms.EmailField(label='邮箱')
    is_active = forms.BooleanField(required=True, label='是否激活')
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label='角色')
    phone = forms.CharField(max_length=20, required=False, label='电话')
    wechat = forms.CharField(max_length=50, required=False, label='微信')
    comment = forms.CharField(max_length=50, required=False, label='备注')
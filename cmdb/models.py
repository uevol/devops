# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

class Common(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        abstract = True

class CiCategory(Common):
    ''' configration item category model '''
    show_in_left = models.BooleanField(default=True)
    is_must = models.BooleanField(default=False)
    url = models.CharField(max_length=200)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def get_url(self):
        return '/cmdb/' + self.code

    class Meta:
        db_table = 'cmdb_ci_category'
    
    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

class CiProperty(Common):
    ''' configration item property model '''
    FORM_TYPE_CHOICE = (("optional", "可选"), ("required", "必填"))
    VALUE_TYPE_CHOICE = (("num", "数值"), ("str", "字符"), ("array", "数组"))
    form_type = models.CharField(max_length=30, choices=FORM_TYPE_CHOICE, default="optional")
    value_type = models.CharField(max_length=30, choices=VALUE_TYPE_CHOICE, default="str")
    is_must = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=True)
    show_in_table = models.BooleanField(default=True)
    is_search = models.BooleanField(default=True)
    ci_category = models.ForeignKey(CiCategory, on_delete=models.CASCADE)
    optional_value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cmdb_ci_property'

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def get_optional_value(self):
        value_list = []
        if self.optional_value:
            value_list = [ value.strip() for value in self.optional_value.split(';')]
        return value_list

    def get_value_type_choice(self):
        return self.VALUE_TYPE_CHOICE


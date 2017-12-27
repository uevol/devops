# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class File(models.Model):
	FILE_TYPE_CHOICE = (("script", "脚本"), ("state", "模块"), ("other", "其他"))
	code               = models.CharField(max_length=100)
	name               = models.CharField(max_length=100)
	file_type          = models.CharField(max_length=100, default="other")
	created_by         = models.CharField(max_length=80,blank=True,null=True)
	comment            = models.CharField(max_length=200,blank=True,null=True)
	create_time        = models.DateTimeField(auto_now_add=True)
	update_time        = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'ops_file'

	def __unicode__(self):
		return self.name		
 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Perm(models.Model):
    ''' custom permission '''
    module = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        ''' class meta info '''
        db_table = 'cus_permission'

    def __str__(self):
        return self.name


class Role(models.Model):
    ''' user role '''
    name = models.CharField(max_length=30, unique=True)
    users = models.ManyToManyField(User)
    perms = models.ManyToManyField(Perm, blank=True)

    class Meta:
        ''' class meta info '''
        db_table = 'user_role'

    def __str__(self):
        return self.name


class Profile(models.Model):
    ''' user profile '''
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    wechat = models.CharField(max_length=30, blank=True)
    comment = models.TextField(max_length=100, blank=True)

    class Meta:
        ''' class meta info '''
        db_table = 'user_profile'

    def __str__(self):
        return self.comment


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    '''create or update user profile '''
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Service(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField(blank=True)
    path = models.CharField(max_length=200, blank=True)
    user = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    comment = models.TextField(max_length=100, blank=True)

    class Meta:
        ''' class meta info '''
        db_table = 'admins_service'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models


class List(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    items_list = models.ForeignKey(List)

    def __str__(self):
        return self.name

class Invites(models.Model):
    email = models.EmailField()
    list_to_invite = models.ForeignKey(List)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.email


''' when new user is created a new List object named "user_default_list" is created, user is added to
this List ManyToMany field and the list is set as users active_list '''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='tojemoja')
    active_list = models.ForeignKey(List, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_default_list = List(name='user_default_list')
        user_default_list.save()
        Profile.objects.create(user=instance, active_list=user_default_list)
        instance.profile.save()
        user_default_list.users.add(instance)
        user_default_list.save()
        #check if there are list invites for this user (email)
        if instance.email:
            for invite in Invites.objects.filter(email=instance.email):
                my_list = invite.list_to_invite
                my_list.users.add(instance)
                my_list.save()
            

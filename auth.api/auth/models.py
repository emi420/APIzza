# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Auth API permission model
class AuthPermission(models.Model):
    objid = models.CharField(max_length=255,unique=True)
    user = models.CharField(max_length=255,unique=False)
    user_permissions = models.CharField(max_length=255,unique=False)
    other_permissions = models.CharField(max_length=255,unique=False)

    def __unicode__(self):
        return self.objid

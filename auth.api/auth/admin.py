# -*- coding: utf-8 -*-

from django.contrib import admin
from auth.models import AuthPermission

class AuthPermissionAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuthPermission, AuthPermissionAdmin)

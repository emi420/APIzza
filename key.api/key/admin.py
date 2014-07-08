# -*- coding: utf-8 -*-

from django.contrib import admin
from key.models import App, AppPermission

class AppAdmin(admin.ModelAdmin):
    pass

class AppPermissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(App, AppAdmin)
admin.site.register(AppPermission, AppPermissionAdmin)

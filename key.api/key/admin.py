# -*- coding: utf-8 -*-

from django.contrib import admin
from key.models import App


class AppAdmin(admin.ModelAdmin):
    pass






admin.site.register(App, AppAdmin)

# -*- coding: utf-8 -*-
from django.db import models

class App(models.Model):
    
    id_aplicacion = models.CharField(max_length=255,unique=True)
    api_key = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    dominio = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Encuesta, Pregunta, Item


#Aqui se registran nuestros modelos
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Item)

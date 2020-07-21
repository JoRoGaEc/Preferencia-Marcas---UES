  # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.


class Administrador(models.Model):
    idUsuario = models.IntegerField( primary_key=True)
    nombreUsuario = models.CharField(max_length=20)
    passUsuario = models.CharField(max_length=30)




class Estadistico(models.Model):
    #ok good
    nombreEst=models.CharField(max_length=50)
    nivelDeConfianza = models.DecimalField(max_digits=2, decimal_places=2)
    errorMuestreo = models.DecimalField(max_digits=2, decimal_places=2)
    tamanoDePoblacion = models.IntegerField()
    muestra = models.IntegerField(default=1)

    def __unicode__(self):
        return '{}'.format(self.nombreEst)

class Encuesta(models.Model):
    estadistico = models.ForeignKey(Estadistico, null=True, blank=False,on_delete=models.CASCADE) #ok goof
    nombreEncuesta = models.CharField(max_length=100)
    descripEnc = models.CharField(max_length=350)
    fechaCreacion = models.DateField()
    estadoEnc= models.BooleanField(default=False)#por defecto es Falso si selecciona el checkbox sera veradero
    faltantes=models.IntegerField(default=1)
    def __unicode__(self):
        return '{}'.format(self.nombreEncuesta)

class Item(models.Model):  #COntiene las direcciones IP de las personas que han contestado la encuesta
   nombreItem=models.CharField(max_length=40)
   
   def __unicode__(self):
        return '{}'.format(self.nombreItem)

class Pregunta(models.Model):
    encuesta = models.ManyToManyField(Encuesta) # para poder asociar las preguntas a la encuesta que deseemos
    descripcion = models.CharField(max_length=150) #descripcion de la Pregunta
    item = models.ManyToManyField(Item)
    def __unicode__(self):
        return '{}'.format(self.descripcion)



class Encuestado(models.Model):
    ip=models.CharField(max_length=15)
    encuesta_enc=models.ForeignKey(Encuesta)   #llave foranea de para mantener la relacion con  encuesta
    def __unicode__(self):
        return '{}'. format(self.ip)

class Selecciona(models.Model):
  encuestado=models.ForeignKey(Encuestado)
  item = models.ForeignKey(Item)    #Foranea para mantener la relacion con Item
  pregunta=models.ForeignKey(Pregunta)


  class Meta:
    unique_together=(('encuestado','item','pregunta'))  #la combinacion de las tres debe ser unico

class Resultado(models.Model):
    frecuencia=models.IntegerField()
    item=models.ForeignKey(Item)
    pregunta=models.ForeignKey(Pregunta)
    encuesta=models.ForeignKey(Encuesta)
    class Meta:
        unique_together=(('item','pregunta','encuesta'))
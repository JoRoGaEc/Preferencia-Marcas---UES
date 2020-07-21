from django import forms
from .models import Encuesta, Pregunta, Item, Estadistico
from captcha.fields import CaptchaField


'''class  crearEncuestaForm(forms.Form):
    nombreEncuesta=forms.CharField(max_length=20)
    descripEnc = forms.CharField(max_length=20)
    fechaCreacion=forms.DateField()
    estadoEnc = forms.BooleanField()
    estadistico=forms.CheckboxSelectMultiple()
'''
class crearEncuestaForm(forms.ModelForm):
    class Meta:
        model=Encuesta
        exclude=['faltantes']
        fields=[
            'nombreEncuesta',
            'descripEnc',
            'fechaCreacion',
            'estadoEnc',
            'estadistico',
        ]
        widgets={
            'nombreEncuesta':forms.TextInput(attrs={'class':'form-control'}),
            'descripEnc':forms.TextInput(attrs={'class':'form-control'}),
            'fechaCreacion':forms.SelectDateWidget(),
            'estadoEnc':forms.CheckboxInput(attrs={'class':'form-control'}),
            'estadistico':forms.Select(),

        }

class crearPreguntaForm(forms.ModelForm):
    class Meta:
        model=Pregunta
        fields=[
            'descripcion',
            'encuesta',
            'item',
        ]

        widgets={
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'encuesta':forms.SelectMultiple(attrs={'class':'form-control'}),
            'item':forms.SelectMultiple(attrs={'class':'form-control'}),
        }
class crearItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=[
              'nombreItem',
        ]

        widgets={
            'nombreItem':forms.TextInput(attrs={'class':'form-control'}),
            
        }
class CrearEstadisticoForm(forms.ModelForm):
    class Meta:
        model=Estadistico
        exclude=['muestra','tamanoDePoblacion', 'nivelConfianza','errorMuestreo']
        fields=[
            'nombreEst',
        

        ]
        widgets={
            'nombreEst':forms.TextInput(attrs={'class':'form-control'}),
           
        }



class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()
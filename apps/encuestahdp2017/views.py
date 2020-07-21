# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response,get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import crearEncuestaForm, crearPreguntaForm, crearItemForm, CrearEstadisticoForm, CaptchaTestForm
from . models import Encuesta, Pregunta,Estadistico, Item,Encuestado,Selecciona,Resultado
#from django.views.generic  import  ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from urllib2 import urlopen  #esto para obtener la direccion ip
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


# Create your views here.\
#Vistas basadas en clases
#Para listar los datos
"""
#prueba 1 para login
def login_page(request):
    message=None
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message= "Tus credenciales son correctas"
                    return HttpResponseRedirect('/inicio/')
                else:
                    message="Tu usuario esta inactivo"
            else:
                message="Nombre de usuario y/o password incorrecto"
    else:
        form=LoginForm()
    return render(request,'formularios/login.html' ,{'form':form,'message':message})
"""

"""
class listar_encuestas(ListView):
    model=Encuesta
    template_name = 'formularios/lista_encuestas.html'


#Para crear encuestas
class crear_encuesta(CreateView):
    model=Encuesta
    fields=[ 'idEncuesta','nombreEncuesta','descripEnc','fechaCreacion','estado']
    template_name='formularios/gestionarEncuestas.html'
    success_url=reverse_lazy('menu:inicioEncuesta')

class borrar_encuesta(DeleteView):
    model=Encuesta
    template_name='formularios/eliminar_encuesta.html'
    success_url=reverse_lazy('menu:mis_encuestas')

class actualizar_encuesta(UpdateView):
    model=Encuesta
    fields=[ 'idEncuesta','nombreEncuesta','descripEnc','fechaCreacion','estado']
    template_name='formularios/gestionarEncuestas.html'
    success_url=reverse_lazy('menu:mis_encuestas')
    """

#---Aca comienza las vistas involucradas en el caso de USO GestionarEncuestas---------------------------------#

#esta vista muestra el cuestioanrio ... es la unica pantalla que se puede ver sin necesidad  de logueo
def cuestionario(request):
    encuesta=Encuesta.objects.filter(estadoEnc='True')
    contexto={"encuestas":encuesta}
    return render(request,'formularios/cuestionario.html', contexto)  #si se llama esta vista en las url's nos renderizara a la direccion del segundo parametro

def menu(request):   #misma logica que la funcion anterior
    return render(request,'formularios/menu.html')

def gestionarEncuesta(request):   # pantalla donde estan opciones de listar, y crear encuestas
    form=crearEncuestaForm(request.POST or None)    #si el formulario tiene una peticion POST
    if form.is_valid():   #validamos si los datos del formulario son validos
       form_data= form.cleaned_data  # es para obtner los datos del objeto limpio en forma {'campo1','campo2'} esto es interno no se muestra...
       nom= form_data.get("nombreEncuesta") # igual que el anterior
       descrip= form_data.get("descripEnc")
       fecha= form_data.get("fechaCreacion")
       est= form_data.get("estadoEnc")
       estadis=form_data.get("estadistico")
       faltantes=estadis.muestra
        #con lo anteriro ahora podemos instanciar un objecto de el modelo Encuesta pasandole los atributos
        #de la forma campoDelModelo=variableDefinida
       obj= Encuesta(nombreEncuesta=nom,descripEnc=descrip,fechaCreacion=fecha, estadoEnc=est,estadistico=estadis, faltantes=faltantes)
       obj.faltantes=estadis.muestra
       obj.save()
        #lo guardamos en la variable context en forma de diccionario para posteriormente pasarsela al formulario
       return redirect('menu:mis_encuestas')
    context={
             "form":form,
            }

    return render(request,"formularios/gestionarEncuestas.html",context)

#esta vista es para desloguearse
def logout_view(request):
    logout(request)     #logout es una vista que trae por defecto django la cual sirve para limpiar nuestra sesion
    return redirect('accounts/login/') #y redireccionamos a la pagina de login


#esta vista es para listar las encuestas disponibles
def lista_encuestas(request):
    encuesta=Encuesta.objects.all().order_by('pk') #Recuperamos todos los objetos de encuesta ordenamos por ID y los guaramos en la variable encuesta
    contexto={'encuestas':encuesta}    #dicha informacion la mandamos en el contexto como un diccionario
    #info de la forma :  variable= {'variable de contexto':variable de la definicion de la vista }
    return render(request,'formularios/lista_encuestas.html',contexto)

#vista pra eliminar una encuesta
def editar_encuesta(request,id_Encuesta):
    encuesta=Encuesta.objects.get(id=id_Encuesta) #recuperamos la Encuesta que tiene el idEncuesta y lo guardamos en encuesta
    form=crearEncuestaForm(request.POST, request.FILES)
    if request.method == 'POST':   #si el metod es POST
        if form.is_valid():    #verificamos que el formulario sea valido (los datos)

            nombreEncuesta = form.cleaned_data['nombreEncuesta']
            descripEnc = form.cleaned_data['descripEnc']
            fechaCreacion = form.cleaned_data['fechaCreacion']
            estado = form.cleaned_data['estadoEnc']
            #guardamos los datos en el objeto
            encuesta.nombreEncuesta=nombreEncuesta
            encuesta.descripEnc=descripEnc
            encuesta.fechaCreacion=fechaCreacion
            encuesta.estadoEnc=estado
            #fin de guardado
            encuesta.save() #guardamos el objeto del modelo  en la BASE DE DATOS
            return redirect('menu:mis_encuestas')  #redireccionamos a la url donde estan las encuestas
    if request.method == 'GET':       #Si el metodo es GET
            form=crearEncuestaForm(initial= {      #Istanciamos el formulario  colocando en los campos el valor de cada campo....
            'nombreEncuesta':encuesta.nombreEncuesta,
            'descripEnc':encuesta.descripEnc,
            'fechaCreacion':encuesta.fechaCreacion,
            'estadoEnc':encuesta.estadoEnc,
                 })
            contexto={'form':form,'encuesta':encuesta} #se guarda en el contexto
    return render(request,'formularios/gestionarEncuestas.html',{'form':form}) #... y renderizamos el formualario con los datos

def eliminar_encuesta(request,id_Encuesta):
        encuesta=Encuesta.objects.get(id=id_Encuesta) #obtenemos la encuesta con el ID
        info="Eliminar  "
        if request.method =="POST":  #si el metodo es POST
            encuesta.delete()     #El elemento el obejeto sera eliminado
            return redirect('menu:mis_encuestas')  # y redireccionamos a la lista de encuestas
        return render(request,'formularios/eliminar_encuesta.html',{'encuesta':encuesta,'info':info})  #si el metodo fue POST se renderiza el template y le pasamos  el contexto

#----- Sobre AgregarPregunta
'''def agregarPregunta(request):
    info="Pregunta Guardada Correctamente"
    if request.method== "POST":
        form=crearPreguntaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('menu:mis_encuestas')
    else:
        form=crearPreguntaForm

    return render(request,"formularios/agregarPregunta.html",{"form":form})
'''
def agregarPregunta(request):
    if request.method=="POST":
        form=crearPreguntaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('menu:mis_encuestas')
    else:
        form=crearPreguntaForm
    return render(request,'formularios/agregarPregunta.html',{"form":form})




    #--------------------SOBRE GESTIONAR RESPUESTAS----------
def agregarItem(request):
        if request.method=="POST":
            form=crearItemForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('menu:agregarItem')
        else:
            form=crearItemForm
        return render(request,'formularios/gestionarMarcas.html',{"form":form})

def ver_preguntas(request, id_Encuesta):
    pregunta=Pregunta.objects.filter(encuesta__pk=id_Encuesta) #Recuperamos todos los objetos de encuesta ordenamos por ID y los guaramos en la variable encuesta
    contexto={'preguntas':pregunta}    #dicha informacion la mandamos en el contexto como un diccionario
    #info de la forma :  variable= {'variable de contexto':variable de la definicion de la vista }
    return render(request,'formularios/filtro_preguntas.html',contexto)

class editar_pregunta(UpdateView):
    model=Pregunta
    fields=[ 'descripcion','encuesta','item']
    template_name='formularios/agregarPregunta.html'
    success_url=reverse_lazy('menu:listar_preguntas')

def listar_preguntas(request):
    pregunta=Pregunta.objects.all() #Recuperamos todos los objetos de encuesta ordenamos por ID y los guaramos en la variable encuesta
    contexto={'preguntas':pregunta}    #dicha informacion la mandamos en el contexto como un diccionario
    #info de la forma :  variable= {'variable de contexto':variable de la definicion de la vista }
    return render(request,'formularios/listar_preguntas.html',contexto)


class eliminar_pregunta(DeleteView):
    model=Pregunta
    template_name='formularios/eliminar_pregunta.html'
    success_url=reverse_lazy('menu:listar_preguntas')

def encuesta_list(request):
    encuesta=Encuesta.objects.all()
    contexto={'encuestas':encuesta}
    return render(request,'encuesta/cuestionario.html',contexto)

#nuevo----------------------------------
'''def gestionarEncuesta(request):
    if request.method== "POST":
        form=crearEncuestaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('menu:mis_encuestas')
    else:
        form=crearEncuestaForm()

    return render(request,"formularios/gestionarEncuestas.html",{"form":form})
'''

def crearEstadistico(request):
        mensaje="Estadistico Guardado"
        form=CrearEstadisticoForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            print instance.nivelDeConfianza
            nivelC=float(request.POST['nivelConf'])
            e=float(request.POST['error'])
            #asignamos el nivel de confianza, el error de la muestra
            instance.nivelDeConfianza=nivelC
            instance.errorMuestreo=e
            N=6321000
            p=q=0.5
            if nivelC==0.95:
                z=1.96
            else:
                z=1.645
            print nivelC,e,N,p,q,z
            num= (z**2)*p*q*N #NUMERADOR FORMULA
            deno= ((N)*e**2)+((z**2)*p*q)      #DENOMINADOR FORMULA
            n=num/deno
            instance.tamanoDePoblacion=N
            instance.muestra=n
            form.save()
            return redirect('menu:mis_estadisticos')
        
        form=CrearEstadisticoForm()
        contexto={
               "mensaje":mensaje,"form":form
            }
        return render(request,"formularios/crearEstadistico.html",contexto)

class listar_estadistico(ListView):
    model=Estadistico
    template_name = 'formularios/lista_estadistico.html'



class listar_respuestas(ListView):
    model=Item
    template_name = 'formularios/lista_respuestas.html'


class eliminarItem(DeleteView):
    model=Item
    template_name='formularios/eliminarItem.html'
    success_url=reverse_lazy('menu:respuestas')

class eliminarEstadistico(DeleteView):
    model=Estadistico
    template_name='formularios/eliminarItem.html'  #se puede usar la misma de item porque es parecido , solo la confirmacion
    success_url=reverse_lazy('menu:mis_estadisticos')

class actualizar_item(UpdateView):
    model=Item
    fields=[ 'nombreItem']
    template_name='formularios/gestionarMarcas.html'
    success_url=reverse_lazy('menu:respuestas')

#Vista para encuestas disponibles
def filtro_items(request, id_pregunta):
    pregunta=Pregunta.objects.get(id=id_pregunta)
    item=Item.objects.filter(pregunta__pk=id_pregunta) #Recuperamos todos los objetos de encuesta ordenamos por ID y los guaramos en la variable encuesta
    contexto={'items':item,"pregunta":pregunta}    #dicha informacion la mandamos en el contexto como un diccionario
    #info de la forma :  variable= {'variable de contexto':variable de la definicion de la vista }
    return render(request,'formularios/filtro_items.html',contexto)



# ESTA VISTA ES PARA MOSTRAR LA ENCUESTA QUE SE SELECCIONE CON SUS RESPECTIVAS PREGUNTAS

def contestar_cuestionario(request, id_encuesta):
    ip_obt=urlopen('http://ip.42.pl/raw').read()
    #validacion para la ip
    encuesta=Encuesta.objects.get(id=id_encuesta)  #obtenemos la encuesta que se va a resolver 
    
    print "Ip obtenida"
    print ip_obt
    try:
        obj=Encuestado.objects.get(ip=ip_obt,encuesta_enc=encuesta)
        print obj 
        mensaje="USTED YA CONTESTO ESA ENCUESTA. SOLO ESTA PERMITIDO CONTESTARLA UNA VEZ" 
    except ObjectDoesNotExist:
        print "Esta ip no se encuentra registrada"
        #encuestado=Encuestado.objects.create(ip=ip_obt,encuesta_enc=encuesta) #creamos la instancia co la ip desde donde se contesto y que encuesta contesto
        pregunta=Pregunta.objects.filter(encuesta__pk=id_encuesta)
        #item=Item.objects.filter(pregunta__encuesta__pk=id_encuesta)
        return render(request,'formularios/resolver.html',{"encuesta":encuesta, "preguntas":pregunta,"encuestado":encuestado})
   
    encuesta=Encuesta.objects.filter(estadoEnc='True')
    contexto={"encuestas":encuesta,"mensaje":mensaje}
    return render(request,'formularios/cuestionario.html', contexto)
    
    #paginador=Paginator(pregunta,2)


    

def encuestado(request):
    if request.method=="POST":
        ip_obt=urlopen('http://ip.42.pl/raw').read() # si el metodo es post , quiere decir que envio los resultados 
        nom=request.POST['nombreEncuesta']  #obtenemos el nombre de la encuesta desde el template
        encuesta=Encuesta.objects.get(nombreEncuesta=nom) #obtenemos la instancia de la encuesta a traves del nombre
        #Para actualizar las encuestas que quedan por HACER
        encuesta.faltantes-=1
        print encuesta.estadoEnc
        if encuesta.faltantes == 0:
            encuesta.estadoEnc = False
        encuesta.save()
        #---- Se crea la instancia del encuestado
        encuestado=Encuestado.objects.create(ip=ip_obt,encuesta_enc=encuesta) #si se contesta la encuesta se crea la instancia de 
        # el encuestado para guardar su ip y que encuesta contesto a traves de ella   
        id_encuesta=encuesta.id
        preguntas=Pregunta.objects.filter(encuesta__pk=id_encuesta)
        
        #print preguntas.id
        print "nombre de la encuesta"
        print nom   #para desplegar nombre de la encuesta
        print "id de la encuesta"
        print encuesta.id  #el id  de la encuesta 
        for pregunta in preguntas:
            print "id de la pregunta"
            id_preg= pregunta.id  #guadar el id de la pregunta

            #----DATOS QUE NECESITAMOS PARA  CREAR LA INSTANCIA DE SELECCION
            id_post=str(pregunta.id) #CONVERTIR  a string el id para concatenarlo 
            id_seleccion=request.POST['respuesta' + id_post]  #el id e la respuesta seleccionada
            id_encuestado=request.POST['id_encuestado']
            #FIN DE LOS DATOS NECESITADOS AHORA A CREAR LA INSTANCIA 
            
            #--- CREACION DE INFORMACION PARA SABER QUE SE CONTESTO DESDE CADA IP --- O SEA INSTANCIA DE SELECCION
            item=Item.objects.get(id=id_seleccion)
            print "LLEGA AUQSKDLDSKLD"
            selecciona=Selecciona.objects.create(encuestado=encuestado,item=item,pregunta=pregunta)
            #--FIN DE LA SELECCION FALTA VALIDAR SI UN ENCUESTADO CONTESTA DOS CUESTIONARIOS SE LE ASIGNE EL MISMO ID DE ENCUESTADO
            #AUNQUE NO SE QUE TAN NECESARIO SEA 

            #--- INICIO PARA CONTEO DE RESULTADOS 
            #Pimero comprobaremos que no haya una instancia creada acerca de la votacion
            
            try:
                obj=Resultado.objects.get(item=item, pregunta=pregunta,encuesta=encuesta)
                #freq=freq+1
                obj.frecuencia+=1
                obj.save()
            except ObjectDoesNotExist:
                #Si el objeto no existe aun ... no se ha contestado por primera vez
                #Entonces creamos la instancia on frecuencia de 1
                #Aqui hacer un for para inicializar con cero los items que no han sido votados aun
                item_temp = item
                pregunta_temp=pregunta
                #creamos las intancias de los items iniciados con frecuencia cero 
                for item in Item.objects.filter(pregunta__pk=pregunta.pk):
                    freq=0

                    resultado=Resultado.objects.create(frecuencia=freq, item=item, pregunta=pregunta,encuesta=encuesta)
                     #aca creampos las instancias iniciadas en cero 

                #ya esta creado podemos incrementarlo en 1

                obj=Resultado.objects.get(item=item_temp, pregunta=pregunta_temp,encuesta=encuesta)
                obj.frecuencia+=1
                obj.save()

                    
            

    return redirect('cuestionario:cuest')
            
#----PARA VER ESTADISTICOS

def ver_estadisticos(request):
    encuesta=Encuesta.objects.all()
    return render(request,'formularios/estadisticos.html',{"encuestas":encuesta})

def graficos(request, id_encuesta):
    encuesta=Encuesta.objects.get(id=id_encuesta)
    muestra=encuesta.estadistico.muestra #obteniendo el valor la muestra del estadistico
    realizada=muestra-encuesta.faltantes
    faltante= encuesta.faltantes
    pregunta=Pregunta.objects.filter(encuesta__pk=id_encuesta) #obtenemos las preguntas de la encuesta
    
    #item=Item.objects.filter(pregunta__encuesta__pk=id_encuesta) #los items de las preguntas
    resultado=Resultado.objects.filter(encuesta=encuesta)
    
    # diccionarioPreg={ }
    # dicItem_Votos={ }
    # if preguntas:
    #     for pregunta in preguntas:
    #         for item in pregunt.item.all:
    #             if resultado.item.id == item.id and resultado.pregunta.id == pregunta.id:



   

    return render(request,'formularios/graficos.html',{"preguntas":pregunta,"resultados":resultado,"encuesta":encuesta,"realizada":realizada, "faltante":faltante})


def grafica_pregunta(request,id_encuesta,id_pregunta):
    encuesta=Encuesta.objects.get(id=id_encuesta)
    pregunta=Pregunta.objects.get(id=id_pregunta)
    resultado=Resultado.objects.filter(encuesta=encuesta,pregunta=pregunta)

    return render (request,'formularios/grafica_pregunta.html',{"encuesta":encuesta,"pregunta":pregunta,"resultados":resultado })



 

def vista_previa(request, id_encuesta):

    encuesta=Encuesta.objects.get(id=id_encuesta)  #obtenemos la encuesta que se va a resolver 
    pregunta=Pregunta.objects.filter(encuesta__pk=id_encuesta)
   # item=Item.objects.filter(pregunta__encuesta__pk=id_encuesta)

    contexto={"encuesta":encuesta,"preguntas":pregunta}
    return render(request,'formularios/vista_previa.html', contexto)



def vista_encuestas(request):
    encuesta=Encuesta.objects.all().order_by('pk') #Recuperamos todos los objetos de encuesta ordenamos por ID y los guaramos en la variable encuesta
    contexto={'encuestas':encuesta}    #dicha informacion la mandamos en el contexto como un diccionario
    #info de la forma :  variable= {'variable de contexto':variable de la definicion de la vista }
    return render(request,'formularios/vista_encuestas.html',contexto)


def previo(request):
    return render(request,'formularios/recaptcha.html')

def resetear_encuesta(request,id_encuesta):  
        encuesta=Encuesta.objects.get(id=id_encuesta) #obtenemos la encuesta con el ID
        info="Seguro eliminar las estadisticas recolectadas en esta encuesta  "
        if request.method =="POST":  #si el metodo es POST
            #encuesta.delete()     #El elemento el obejeto sera eliminado

            encuesta.faltantes=encuesta.estadistico.muestra
            encuesta.save()
            Encuestado.objects.filter(encuesta_enc=encuesta).delete()
            Resultado.objects.filter(encuesta=encuesta).delete()
            return redirect('menu:ver_estadisticos')  # y redireccionamos a la lista de encuestas
        return render(request,'formularios/eliminar_encuesta.html',{'encuesta':encuesta,'info':info})  #si el metodo fue POST se renderiza el template y le pasamos  el contexto



def captcha(request,id_encuesta):
    idEnc=id_encuesta
    form=CaptchaTestForm()
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('cuestionario:resolver',args=(idEnc,)))
        # else: 
        #      return HttpResponseRedirect(reverse('cuestionario:resolver',args=(idEnc,)))
    return render(request,'formularios/captcha.html',{"form":form,"idEnc":idEnc})
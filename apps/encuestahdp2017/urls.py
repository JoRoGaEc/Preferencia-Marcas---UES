from django.conf.urls import url, include
from .views import captcha,resetear_encuesta,eliminarEstadistico,listar_estadistico,previo,vista_encuestas,vista_previa,grafica_pregunta,graficos,ver_estadisticos,encuestado, contestar_cuestionario,filtro_items, actualizar_item,eliminarItem,listar_respuestas,crearEstadistico,agregarPregunta, gestionarEncuesta , menu,logout_view, agregarItem, cuestionario,lista_encuestas,editar_encuesta, eliminar_encuesta, ver_preguntas, listar_preguntas,eliminar_pregunta, editar_pregunta,encuesta_list
from django.contrib.auth.decorators import login_required


urlpatterns = [

   #url(r'^salir',logout_view,name='salir'),
    #url(r'^gestionMarca',login_required(gestionarRespuesta),name='inicioMarca'),
    url(r'^gestionEncuesta',login_required(gestionarEncuesta), name='inicioEncuesta'),
    #url(r'^login',login_page),
    url(r'^$',cuestionario, name='cuest'),
    url(r'^listar$',encuesta_list,name='encuesta_persona'),
    url(r'^lista/encuestas/',login_required(lista_encuestas), name='mis_encuestas'),
    url(r'^lista/ver_preguntas/(?P<id_Encuesta>\d+)/$',login_required(ver_preguntas), name='ver_preguntas'),
    url(r'^editar/(?P<id_Encuesta>\d+)/$',login_required(editar_encuesta), name='editar_encuesta'),
    url(r'^eliminar/(?P<id_Encuesta>\d+)/$',login_required(eliminar_encuesta), name='eliminar_encuesta'),
    url(r'^agregar_pregunta/',login_required(agregarPregunta), name='agregarPregunta'),
    url(r'^index/',login_required(menu), name='index'),

    #nuevas
    url(r'^editar/pregunta/(?P<pk>\d+)/$',login_required(editar_pregunta.as_view()), name='editar_pregunta'),  #esta es una vista hecha basandose en clasess
    url(r'^eliminar/pregunta/(?P<pk>\d+)/$',login_required(eliminar_pregunta.as_view()), name='eliminar_pregunta'),

    url(r'^preguntas/listar_preguntas/',login_required(listar_preguntas), name='listar_preguntas'),
    url(r'^gestionEstadico',login_required(crearEstadistico), name='estadisticos'),
    url(r'^agregarItem/',login_required(agregarItem), name='agregarItem'), # agregarITem
    url(r'^preguntas/respuestas/',login_required(listar_respuestas.as_view()), name='respuestas'),
    url(r'^borrar/Item/(?P<pk>\d+)/$',login_required(eliminarItem.as_view()), name='eliminar_respuesta'), # eliminarItem
    url(r'^actualizar/Item/(?P<pk>\d+)/$',login_required(actualizar_item.as_view()), name='actualizar_item'), # eliminarItem

    url(r'^ver/items/(?P<id_pregunta>\d+)/$',login_required(filtro_items), name='ver_items'),

    url(r'^resolver/(?P<id_encuesta>\d+)/$',contestar_cuestionario, name='resolver'),
    url(r'^encuestado/',encuestado, name='votacion'),

    url(r'^graficos/(?P<id_encuesta>\d+)/$',login_required(graficos), name='graficos'),
    ##para  ver estadisticos
    url(r'^ver_estadisticos/',login_required(ver_estadisticos), name='ver_estadisticos'),
    #url(r'^grafica_pregunta/(?P<id_encuesta>\d+)/g/(?P<id_pregunta>\d+)/$',grafica_pregunta, name='grafica_pregunta'),
    url(r'^grafica_pregunta/(?P<id_encuesta>[0-9]+)/(?P<id_pregunta>[0-9]+)/',login_required(grafica_pregunta), name='grafica_pregunta'),
    #para vista previa
    url(r'^vista_previa/(?P<id_encuesta>\d+)/$',login_required(vista_previa), name='vista_previa'),

    url(r'^vista_encuestas/',login_required(vista_encuestas), name='vista_encuestas'), 
    url(r'^recaptcha/',previo, name='previo'), 

    url(r'^estadisticos/',login_required(listar_estadistico.as_view()), name='mis_estadisticos'),
    url(r'^delete/estadistico/(?P<pk>\d+)/$',login_required(eliminarEstadistico.as_view()), name='eliminar_estadistico'), # eliminarItem
    url(r'^resetear/(?P<id_encuesta>\d+)/$',resetear_encuesta, name='resetear'), # eliminarItem
    url(r'^captcha/(?P<id_encuesta>\d+)/$',captcha, name='captcha'), # eliminarItem



]

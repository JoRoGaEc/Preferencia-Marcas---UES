"""preferenciaMarcaEmbutidos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin

from django.contrib.auth.views import login, logout_then_login, logout

#from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^inicio/',include('apps.encuestahdp2017.urls' )),
    url(r'^menu/',include('apps.encuestahdp2017.urls', namespace='menu')),
    #url(r'^encuesta/', include('apps.encuestahdp2017.urls', namespace='gestionarEncuesta')),
    #url(r'^cuenta/', include('apps.encuestahdp2017.urls')),
    #url(r'^marcas/', include('apps.encuestahdp2017.urls', namespace='marcas')),
    url(r'^accounts/login/',login,{'template_name':'formularios/login.html'}, name='login'),
    url(r'^logout/',logout_then_login, name='logout'),
    url(r'^cuestionario/',include('apps.encuestahdp2017.urls', namespace='cuestionario')),


]

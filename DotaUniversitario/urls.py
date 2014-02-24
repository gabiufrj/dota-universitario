#encoding:utf-8

from django.conf.urls import patterns, include, url
from DotaUniversitario import views
from noticias import views as noticias_views
from campeonatos import views as campeonatos_views
from ligas import views as ligas_views
from universidades import views as universidades_views
from times import views as times_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^home/$', views.home),
    url(r'^sobre/$', views.about),
    url(r'^copa-minerva/(\d+)/$', views.copa_minerva),
    
    # campeonatos
    url(r'^campeonatos/todos/$', campeonatos_views.todos),
    url(r'^campeonatos/andamento/$', campeonatos_views.em_andamento),
    url(r'^campeonatos/inscricoes-abertas/$', campeonatos_views.inscricoes_abertas),
    url(r'^campeonatos/terminados/$', campeonatos_views.terminados),
    url(r'^campeonatos/crie-o-seu/$', campeonatos_views.criar),
    url(r'^campeonatos/(\d+)/$', campeonatos_views.visualizar),
    
    # ligas
    url(r'^ligas/ufrj/$', views.liga_ufrj),
    url(r'^ligas/(\d+)/$', ligas_views.visualizar),
    
    # universidades
    
    # times
    url(r'^times/(\d+)/$', times_views.visualizar),
    
    # notícias
    url(r'^noticias/(\d+)/$', noticias_views.noticia_simples),
    url(r'^noticias/$', noticias_views.todas),
    
    # Examples:
    # url(r'^$', 'DotaUniversitario.views.home', name='home'),
    # url(r'^DotaUniversitario/', include('DotaUniversitario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

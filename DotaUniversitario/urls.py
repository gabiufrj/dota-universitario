#encoding:utf-8

from django.conf.urls import patterns, include, url
from DotaUniversitario import views
from noticias import views as noticias_views
from campeonatos import views as campeonatos_views
from ligas import views as ligas_views
from universidades import views as universidades_views
from times import views as times_views
from usuarios import views as usuarios_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^home/$', views.home),
    url(r'^sobre/$', views.about),
    url(r'^login/$', views.login),
    url(r'^cadastro/$', views.cadastro),
    url(r'^logout/$', views.logout),
    
    # campeonatos
    url(r'^campeonatos/todos/$', campeonatos_views.todos),
    url(r'^campeonatos/andamento/$', campeonatos_views.em_andamento),
    url(r'^campeonatos/inscricoes-abertas/$', campeonatos_views.inscricoes_abertas),
    url(r'^campeonatos/terminados/$', campeonatos_views.terminados),
    url(r'^campeonatos/crie-o-seu/$', campeonatos_views.criar),
    url(r'^campeonatos/(\d+)/$', campeonatos_views.visualizar),
    url(r'^campeonatos/(\d+)/inscricao/$', campeonatos_views.inscrever),
    
    # ligas
    url(r'^ligas/(\d+)/$', ligas_views.visualizar),
    
    # universidades
    
    # times
    url(r'^times/(\d+)/$', times_views.visualizar),
    url(r'^times/meus-times/$', times_views.todos_por_usuario),
    url(r'^times/criar/$', times_views.criar),
    url(r'^times/(\d+)/adicionar_membro/$', times_views.inserir_membro),
    url(r'^times/(\d+)/sair/$', times_views.sair),
    
    # partidas
    url(r'^partidas/(\d+)/$', campeonatos_views.visualizar_partida),
    url(r'^partidas/(\d+)/gerar-senha/$', campeonatos_views.partida_gerar_senha),
    
    # notícias
    url(r'^noticias/$', noticias_views.todas),
    url(r'^noticias/(\d+)/$', noticias_views.noticia_simples),
    url(r'^noticias/minhas/$', noticias_views.todas_proprias),
    url(r'^noticias/criar/$', noticias_views.nova_noticia),    
    
    # usuários
    url(r'^usuarios/(.+)/$', usuarios_views.visualizar),
    
    # Examples:
    # url(r'^$', 'DotaUniversitario.views.home', name='home'),
    # url(r'^DotaUniversitario/', include('DotaUniversitario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # WYSIWYG editor
    url(r'^summernote/', include('django_summernote.urls')),
)

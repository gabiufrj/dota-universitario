from django.conf.urls import patterns, include, url
from DotaUniversitario import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^home/$', views.home),
    url(r'^hello/$', views.hello),
    url(r'^sobre/$', views.about),
    url(r'^copa-minerva/(\d+)/$', views.copa_minerva),
    url(r'^campeonatos/andamento/$', views.todos_campeonatos_em_andamento),
    url(r'^campeonatos/inscricoes-abertas/$', views.todos_campeonatos_inscricoes_abertas),
    url(r'^campeonatos/terminados/$', views.todos_campeonatos_terminados),
    url(r'^campeonatos/crie-o-seu/$', views.campeonatos_criacao),
    
    # Examples:
    # url(r'^$', 'DotaUniversitario.views.home', name='home'),
    # url(r'^DotaUniversitario/', include('DotaUniversitario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

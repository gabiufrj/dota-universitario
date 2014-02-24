#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render
from noticias.models import Noticia
    
def home(request):
    # pega as notícias do banco
    noticias = Noticia.objects.all()[0:4]
    return render(request, 'index.html', {'lista_noticias': noticias})
    
def about(request):
    return render(request, 'about.html', {})
    
def copa_minerva(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    return render(request, 'segunda.html', {})
    
    raise Http404()
    
def liga_ufrj(request):
    return render(request, 'liga-template.html', 
        {'liga_nome': 'UFRJ',
         'liga_universidade_sigla': 'UFRJ',
         'liga_administrador': 'alguém',
         'liga_criacao': '05/04/1857',
         'liga_campeonatos': '27',
         'liga_camp_andamento': False,
         'liga_camp_agendados': True,
        })
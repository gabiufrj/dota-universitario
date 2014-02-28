#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from noticias.models import Noticia

def noticia_simples(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera notícia no banco
    try:
        noticia = Noticia.objects.get(id=id)
    except Noticia.DoesNotExist:
        raise Http404()
        
    return render(request, 'noticia-template.html', 
                    {
                        'noticia_titulo': noticia.titulo,
                        'noticia_conteudo': noticia.conteudo,
                        'noticia_autor': noticia.autor,
                        'noticia_criacao': noticia.data_criacao,
                        'noticia_edit': noticia.data_editado,
                    }, context_instance=RequestContext(request)
                 )


def todas(request):
    lista_noticias = Noticia.objects.order_by("-data_criacao")
    return render(request, 'noticias-todas-template.html', 
                    {
                        'lista_noticias': lista_noticias,
                    }, context_instance=RequestContext(request)
                )
#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext

from usuarios.models import Usuario

def visualizar(request, nome):
    # tenta pegar usuário com o username passado
    try:
        usuario = Usuario.objects.get(user__username=nome)
    except Usuario.DoesNotExist:
        raise Http404()

    return render(request, 'usuario-visualizar.html', 
                    {
                        'usuario': usuario,
                    }, 
                    context_instance=RequestContext(request)
                 )
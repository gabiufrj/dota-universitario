#encoding:utf-8

from datetime import datetime 

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext

from usuarios.models import Usuario

from noticias.models import Noticia, Comentario

from noticias.forms import CriarComentarioForm, CriarNoticiaForm


def cria_comentario(username, noticia_id, data):
    try:
        texto = data['texto']
    except:
        return False
        
    # Pega a noticia correta
    try:
        noticia = Noticia.objects.get(id=noticia_id)        
    except Noticia.DoesNotExist:
        return False
     
    # Verifica se o usuario existe
    try:
        usuario = Usuario.objects.get(user__username=username)
    except Usuario.DoesNotExist:
        return False
        
    # cria objeto de comentário
    comment = Comentario()
    comment.user = usuario
    comment.noticia = noticia
    comment.data_criacao = datetime.now()
    comment.data_editado = datetime.now()    
    comment.conteudo = texto
    
    comment.save()
    
    return True

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
        
    # Verifica se algum comentário foi enviado agora
    sucesso = 0
    if request.method == 'GET':
        form = CriarComentarioForm()
    else:
        form = CriarComentarioForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if cria_comentario(request.user.username, id, form_data):
                sucesso = 1
            else:
                sucesso = -1
        
    # recupera comentários no banco
    comentarios = Comentario.objects.filter(noticia=noticia)
    
    return render(request, 'noticia-template.html', 
                    {
                        'noticia': noticia,
                        'comentarios': comentarios,
                        'comentario_form': form,
                        'sucesso': sucesso,
                    }, context_instance=RequestContext(request)
                 )


def todas(request):
    lista_noticias = Noticia.objects.order_by("-data_criacao")
    return render(request, 'noticias-todas-template.html', 
                    {
                        'lista_noticias': lista_noticias,
                    }, context_instance=RequestContext(request)
                )
                
                
def todas_proprias(request):
    lista_noticias = Noticia.objects.filter(autor=request.user.username).order_by("-data_criacao")
    return render(request, 'noticias-todas-template.html', 
                    {
                        'lista_noticias': lista_noticias,
                    }, context_instance=RequestContext(request)
                )



def cria_noticia(username, data):
    try:
        texto = data['texto']
        titulo = data['titulo']
        resumo = data['resumo']
    except:
        return False
        
    # Verifica se o usuario existe
    try:
        usuario = Usuario.objects.get(user__username=username)
    except Usuario.DoesNotExist:
        return False
        
    # cria objeto de comentário
    noticia = Noticia()
    noticia.autor = usuario
    noticia.titulo = titulo
    noticia.conteudo = texto
    noticia.resumo = resumo
    noticia.data_criacao = datetime.now()
    noticia.data_editado = datetime.now()
    
    try:
        noticia.save()
    except:
        return False

    return True

@login_required()    
def nova_noticia(request):
    sucesso = 0
    if request.method == 'GET':
        form = CriarNoticiaForm()
    else:
        form = CriarNoticiaForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if cria_noticia(request.user.username, form_data):
                messages.success(request, 'Notícia inserida com sucesso!')
                return redirect('/noticias/minhas/')
            else:
                messages.error(request, 'Erro interno ao cadastrar notícia, tente novamente mais tarde =/.')
                sucesso = -1
        else:
            messages.error(request, 'Parece que tem algo errado com sua notícia, confira ou contate-nos.')
                
    return render(request, 'noticia-criar.html', 
                    {
                        'noticia_form': form,
                        'sucesso': sucesso,
                    }, context_instance=RequestContext(request)
                )
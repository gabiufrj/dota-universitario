#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.template import RequestContext
from noticias.models import Noticia
    
def home(request):
    # pega as notícias do banco
    noticias = Noticia.objects.all()[0:4]
    
    return render(request, 'index.html', 
                        {'lista_noticias': noticias,
                        }, context_instance=RequestContext(request))
    
def about(request):
    user = request.user

    return render(request, 'about.html', {}, context_instance=RequestContext(request))
    
def login(request):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {}, context_instance=RequestContext(request))
        else:
            return render(request, 'login.html', {}, context_instance=RequestContext(request))
    
    if request.method == 'GET':
        return render(request, 'login.html', {}, context_instance=RequestContext(request))
    
def logout(request):
    auth.logout(request)
    
    return redirect('/')
    
def cadastro(request):
    return render(request, 'cadastro.html', {}, context_instance=RequestContext(request))
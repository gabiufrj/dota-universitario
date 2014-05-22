#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages

from noticias.models import Noticia
from usuarios.models import Usuario
from universidades.models import Universidade
from DotaUniversitario.forms import CadastroForm, CadastroModelForm
    
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
    
def create_user(request, form_cleaned_data):
    try:
        username = form_cleaned_data['username']
        senha = form_cleaned_data['password']
        email = form_cleaned_data['email']
        universidade = form_cleaned_data['universidade']
    except:
        return False
        
    user_novo, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user_novo.set_password(senha)
        user_novo.save()
    
    uni = Universidade.objects.get(id=universidade)
    usuario_novo, created = Usuario.objects.get_or_create(user=user_novo, universidade=uni)

    user = auth.authenticate(username=username, password=senha)
    if user is not None:
        auth.login(request, user)        
        return True
    
    return False
    
def cadastro(request):
    if request.method == 'GET':
        form = CadastroForm()
    else:
        form = CadastroForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if create_user(request, form_data):
                messages.success(request, 'Cadastro realizado com sucesso. Bem-vindo!')
                return redirect('/')
            else:
                messages.error(request, 'Erro interno ao cadastrar usuário, tente novamente mais tarde =/.')
        else:
            messages.error(request, 'Parece que há algo errado com seu cadastro, confira-o e tente novamente =).')
    
    return render(request, 'cadastro.html', {'cadastro_form': form}, context_instance=RequestContext(request))
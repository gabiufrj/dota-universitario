#encoding: utf-8

from times.models import Time, Contrato
from usuarios.models import Usuario
from universidades.models import Universidade
from times.forms import CriarTimeForm, InserirMembroForm

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime

def visualizar(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera time no banco
    try:
        time = Time.objects.get(id=id)
        membros = Contrato.objects.filter(time=time)
    except Time.DoesNotExist:
        raise Http404()
        
    # verifica se o usuário é membro do time
    integrante = False
    try:
        contrato = Contrato.objects.get(user__user__username=request.user.username, time__id=id)
        integrante = True
    except Contrato.DoesNotExist:
        integrante = False
        
    # verifica se o usuário é capitão do time
    capitao = False
    try:
        contrato = Contrato.objects.get(user__user__username=request.user.username, time__id=id)
        capitao = contrato.capitao
    except Contrato.DoesNotExist:
        capitao = False
    
    return render(request, 'time-visualizar.html', 
                    {
                        'time': time, 
                        'membros': membros,
                        'capitao': capitao,
                        'integrante': integrante,
                    }, context_instance=RequestContext(request))
    
def todos_por_usuario(request):
    if request.user.is_authenticated():
        try:
            usuario = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            return redirect('/login/')
    else:
        return redirect('/login/')
        
    contratos = Contrato.objects.filter(user=usuario)    

    return render(request, 'time-todos-usuario.html', 
                    {
                        'contratos': contratos,
                    }, context_instance=RequestContext(request))
         

def cria_time(username, form_data):
    try:
        form_nome = form_data['nome']
        form_sigla = form_data['sigla']
        universidade = form_data['universidade']
    except:
        return False

    # Pega a universidade escolhida, pelo id
    uni = Universidade.objects.get(id=universidade)

    # Cria o time
    time_novo, created = Time.objects.get_or_create(nome=form_nome, sigla=form_sigla, universidade=uni)    
    
    # Associa o usuario ao time
    try:
        usuario = Usuario.objects.get(user__username=username)
    except Usuario.DoesNotExist:
        return False
        
    contrato = Contrato()
    contrato.user = usuario
    contrato.time = time_novo
    contrato.capitao = True
    contrato.save()
    
    return True
         
@login_required
def criar(request):
    if request.method == 'GET':
        form = CriarTimeForm()
    else:
        form = CriarTimeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if cria_time(request.user.username, form_data):
                return redirect('/times/meus-times/')
    
    return render(request, 'time-criar.html', {'time_form': form}, context_instance=RequestContext(request))
    


def insere_membro(username, time_id, form_data):
    # pegar informações do form
    try:
        form_novo_username = form_data['nome']
    except:
        return False
        
    # checar se o usuário é capitão do time
    try:
        contrato = Contrato.objects.get(user__user__username=username, time__id=time_id)
        capitao = contrato.capitao
    except Contrato.DoesNotExist:
        return False
        
    if capitao == False:
        return False
        
    time = Time.objects.get(id=time_id)
    novo_membro = Usuario.objects.get(user__username=form_novo_username)
    contrato = Contrato()
    contrato.time = time
    contrato.user = novo_membro
    contrato.save()
    
    return True
    
@login_required
def inserir_membro(request, id):
    capitao = True
    
    # checa se o id é um número e existe um time associado de fato
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    try:
        time = Time.objects.get(id=id)
    except Time.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        # checar se o usuário é capitão do time
        try:
            contrato = Contrato.objects.get(user__user__username=request.user.username, time__id=id)
            capitao = contrato.capitao
        except Contrato.DoesNotExist:
            raise Http404()
            
        form = InserirMembroForm(initial={'time_id': id})
    else:
        form = InserirMembroForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if insere_membro(request.user.username, id, form_data):
                redirect_url = u'/times/{0}/'.format(id)
                return redirect(redirect_url)

    return render(request, 'time-inserir-membro.html', 
                    {
                        'time_inserir_form': form,
                        'time': time,
                        'capitao': capitao,
                    }, context_instance=RequestContext(request))

                    
@login_required
def sair(request, id):
    # confere se o id é inteiro e tem um time associado
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    try:
        time = Time.objects.get(id=id)
    except Time.DoesNotExist:
        raise Http404()
        
    # confere se existe um contrato entre time e jogador
    try:
        contrato = Contrato.objects.get(user__user__username=request.user.username, time__id=id)
    except Contrato.DoesNotExist:
        redirect_url = u'/times/{0}/'.format(id)
        return redirect(redirect_url)
        
    contrato.delete()
    redirect_url = u'/times/{0}/'.format(id)
    return redirect(redirect_url)
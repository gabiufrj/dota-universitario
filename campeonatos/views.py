#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime

from campeonatos.models import Campeonato, Inscricao
from times.models import Time, Contrato

def todos(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))

def em_andamento(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(inicio_partidas__lte=hoje, fim_partidas__gte=hoje)
    return render(request, 'camp-andamento.html', 
                    {'lista_campeonatos': lista_campeonatos,
                    }, context_instance=RequestContext(request)
                )
    
def inscricoes_abertas(request):
    return render(request, 'camp-inscricoes-abertas.html', {},
                    context_instance=RequestContext(request)
                )
    
def terminados(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(fim_partidas__lt=hoje)
    return render(request, 'camp-terminados.html', 
                    {'lista_campeonatos': lista_campeonatos,
                    }, context_instance=RequestContext(request)
                )
    
def visualizar(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera campeonato no banco
    try:
        campeonato = Campeonato.objects.get(id=id)
    except Campeonato.DoesNotExist:
        raise Http404()
        
    # recupera inscricoes do campeonato
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    
    # verifica se as inscrições estão abertas
    hoje = datetime.date.today()
    inscricoes_abertas = False
    if campeonato.fim_inscricoes >= hoje:
        if campeonato.inicio_inscricoes <= hoje:
            inscricoes_abertas = True
    
    return render(request, 'camp-visualizar.html', 
                    {
                        'campeonato': campeonato,
                        'inscricoes': inscricoes,
                        'inscricoes_abertas': inscricoes_abertas,
                    }, context_instance=RequestContext(request)
                )
                
@login_required()
def inscrever(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera campeonato no banco
    try:
        campeonato = Campeonato.objects.get(id=id)
    except Campeonato.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        # recupera usuário e times que ele é capitão
        contratos = Contrato.objects.filter(user__user__username=request.user.username, capitao=True)
        times = []
        for contrato in contratos:
            times.append(contrato.time)
        
        return render(request, 'camp-inscricao.html', 
                        {
                            'campeonato': campeonato,
                            'times': times,
                        }, context_instance=RequestContext(request)
                    )
    else:
        if 'time' in request.POST and request.POST['time']:
            id_time = request.POST['time']
            # pega o time selecionado
            try:
                time = Time.objects.get(id=id_time)
            except Time.DoesNotExist:
                raise Http404()
            
            # cria inscrição
            inscricao, created = Inscricao.objects.get_or_create(time=time, campeonato=campeonato)
            return redirect('/')
        else:
            raise Http404()
    
@login_required()
def criar(request):
    return render(request, 'camp-inscricoes-abertas.html', {}, 
                    context_instance=RequestContext(request))
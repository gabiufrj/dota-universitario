#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render
import datetime

from campeonatos.models import Campeonato

def todos(request):
    return render(request, 'index.html', {})

def em_andamento(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(inicio_partidas__lte=hoje, fim_partidas__gte=hoje)
    return render(request, 'camp-andamento.html', {'lista_campeonatos': lista_campeonatos})
    
def inscricoes_abertas(request):
    return render(request, 'camp-inscricoes-abertas.html', {})
    
def terminados(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(fim_partidas__lt=hoje)
    return render(request, 'camp-terminados.html', {'lista_campeonatos': lista_campeonatos})
    
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
    
    return render(request, 'camp-visualizar.html', {'campeonato': campeonato})
    
def criar(request):
    return render(request, 'camp-inscricoes-abertas.html', {})
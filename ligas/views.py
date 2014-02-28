#encoding:utf-8

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import datetime

from ligas.models import Liga
from times.models import Time
from campeonatos.models import Campeonato

def visualizar(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    hoje = datetime.date.today
    # recupera liga no banco
    try:
        liga = Liga.objects.get(id=id)
        times = Time.objects.filter(universidade=liga.universidade)
        campeonatos = Campeonato.objects.filter(universidade=liga.universidade, fim_partidas__lt=hoje)
        campeonatos_andamento = Campeonato.objects.filter(universidade=liga.universidade, inicio_partidas__lte=hoje, fim_partidas__gte=hoje)
        campeonatos_agendados = Campeonato.objects.filter(universidade=liga.universidade, inicio_partidas__gt=hoje).order_by("inicio_partidas")
        campeonatos_terminados = Campeonato.objects.filter(universidade=liga.universidade, fim_partidas__lt=hoje).order_by('inicio_partidas')
    except Liga.DoesNotExist:
        raise Http404()

    return render(request, 'liga-template.html', 
                    {'liga': liga, 'lista_times': times,
                    'liga_campeonatos': len(campeonatos),
                    'campeonatos_andamento': campeonatos_andamento, 
                    'campeonatos_agendados': campeonatos_agendados,
                    'campeonatos_terminados': campeonatos_terminados,
                    }, context_instance=RequestContext(request)
                )
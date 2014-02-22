from django.http import Http404, HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world")
    
def home(request):
    return render(request, 'index.html', {})
    
def about(request):
    return render(request, 'about.html', {})
    
def copa_minerva(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    if id == 2:
        return render(request, 'segunda.html', {})
    
    raise Http404()
    
def todos_campeonatos_em_andamento(request):
    return render(request, 'camp_andamento.html', {})
    
def todos_campeonatos_inscricoes_abertas(request):
    return render(request, 'camp_inscricoes_abertas.html', {})
    
def todos_campeonatos_terminados(request):
    raise Http404()
    
def campeonatos_criacao(request):
    raise Http404()
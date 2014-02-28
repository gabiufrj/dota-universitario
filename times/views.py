from times.models import Time, Contrato

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render
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
    
    return render(request, 'time-visualizar.html', 
                    {
                        'time': time, 
                        'membros': membros,
                    }, context_instance=RequestContext(request))
    
def todos_por_usuario(request):
    return render(request, 'time-visualizar.html', 
            {
                
            }, context_instance=RequestContext(request))
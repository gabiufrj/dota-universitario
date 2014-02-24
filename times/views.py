from times.models import Time

from django.http import Http404, HttpResponse
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
    except Time.DoesNotExist:
        raise Http404()
    
    return render(request, 'time-visualizar.html', {'time': time})
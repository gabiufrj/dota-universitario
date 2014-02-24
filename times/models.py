#encoding utf-8

from universidades.models import Universidade
from django.db import models
import datetime

class Time(models.Model):
    nome = models.CharField(max_length=40)
    sigla = models.CharField(max_length=8)
    
    universidade = models.ForeignKey(Universidade)
    
    capitao = models.CharField(max_length=40)
    capitao_email = models.EmailField()
    
    data_criacao = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.nome

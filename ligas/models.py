#encoding:utf-8

from universidades.models import Universidade
from django.db import models
import datetime

class Liga(models.Model):
    nome = models.CharField(max_length=40)
    
    universidade = models.ForeignKey(Universidade)
    
    descricao = models.TextField()
    administrador = models.CharField(max_length=40)
    administrador_email = models.EmailField()
    
    data_criacao = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.nome
#encoding utf-8

from universidades.models import Universidade
from usuarios.models import Usuario
from django.db import models
import datetime    

class Time(models.Model):
    nome = models.CharField(max_length=40)
    sigla = models.CharField(max_length=8)
    
    universidade = models.ForeignKey(Universidade)
    
    data_criacao = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.nome

        
class Contrato(models.Model):
    user = models.ForeignKey(Usuario)
    time = models.ForeignKey(Time)
    
    capitao = models.BooleanField(default=False)
    
    ROLE_ESCOLHAS = (
        ('Support', 'Support'),
        ('Offlaner', 'Offlaner'),
        ('Mid', 'Mid'),
        ('Carry', 'Carry'),
    )
    papel = models.CharField(max_length=15,
                                choices=ROLE_ESCOLHAS,
                                null=True)
                                
    def __unicode__(self):
        return u'{0} - {1}'.format(self.user.user.username, self.time.nome)
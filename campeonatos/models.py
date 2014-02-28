#encoding:utf-8

from universidades.models import Universidade
from times.models import Time
from usuarios.models import Usuario
from django.db import models
import datetime

class Campeonato(models.Model):
    nome = models.CharField(max_length=40)
    criador = models.ForeignKey(Usuario)
    descricao = models.TextField()
    
    data_criacao = models.DateField(auto_now_add=True)
    
    inicio_inscricoes = models.DateField(default=datetime.date.today)
    fim_inscricoes = models.DateField()
    
    inicio_partidas = models.DateField(null=True)
    fim_partidas = models.DateField(null=True)
    
    campeao = models.ForeignKey(Time, null=True, related_name='time_campeao')
    vicecampeao = models.ForeignKey(Time, null=True, related_name='time_vice')
    
    vagas = models.IntegerField()
    
    seletiva = models.BooleanField(default=False)
    
    universidade = models.ForeignKey(Universidade, null=True)
    
    ROUNDROBIN = 'RR'
    PLAYOFFS = 'PL'
    WINNERBRACKET = 'WB'
    FORMATO_ESCOLHAS = (
        (ROUNDROBIN, 'Pontos corridos'),
        (PLAYOFFS, 'Eliminação simples'),
        (WINNERBRACKET, 'Eliminação dupla'),
    )
    formato = models.CharField(max_length=2,
                                choices=FORMATO_ESCOLHAS,
                                default=PLAYOFFS,
                                null=True)
                                
    def formato_to_string():
        if formato:
            if formato == 'RR':
                return 'Pontos corridos'
            if formato == 'PL':
                return 'Eliminação simples'
            if formato == 'WB':
                return 'Eliminação dupla'
                
        return ''

    def __unicode__(self):
        return self.nome
    
    class Meta:
        ordering = ['-inicio_inscricoes']
        
        
class Inscricao(models.Model):
    time = models.ForeignKey(Time)
    campeonato = models.ForeignKey(Campeonato)

    data_inscricao = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return u'{0} - {1}'.format(self.time.nome, self.campeonato.nome)
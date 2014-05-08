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
    
    campeao = models.ForeignKey(Time, null=True, blank=True, related_name='time_campeao')
    vicecampeao = models.ForeignKey(Time, null=True, blank=True, related_name='time_vice')
    
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
        
    def numero_inscricoes(self):
        qtd = Inscricao.objects.filter(campeonato=self).count()
        return qtd
        
    def is_inscricoes_abertas(self):
        hoje = datetime.date.today()
        inscricoes_abertas = False
        if self.fim_inscricoes >= hoje:
            if self.inicio_inscricoes <= hoje:
                inscricoes_abertas = True
                
        return inscricoes_abertas
    
    class Meta:
        ordering = ['-inicio_inscricoes']
        
        
class Inscricao(models.Model):
    time = models.ForeignKey(Time)
    campeonato = models.ForeignKey(Campeonato)

    data_inscricao = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return u'{0} - {1}'.format(self.time.nome, self.campeonato.nome)
        
        
# Fazer classe de "trabalho" em um campeonato (para casters, staff, etc)
        
class Partida(models.Model):
    timeA = models.ForeignKey(Time, related_name='time_a')
    timeB = models.ForeignKey(Time, related_name='time_b')

    campeonato = models.ForeignKey(Campeonato)
    
    # match id, só depois da partida realizada
    match_id = models.CharField(max_length=20, null=True)
    
    data_agendada = models.DateField(null=True)
    data_realizacao = models.DateField(null=True)
    
    vencedor = models.CharField(max_length=40, null=True)
    
    # senha do lobby, que será gerada aleatoriamente, só armazenar
    # depois de alguém criar o lobby via site
    senha_lobby = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ['-data_realizacao', 'data_agendada']
    
    def __unicode__(self):
        return u'{0} vs. {1}'.format(self.timeA.nome, self.timeB.nome)
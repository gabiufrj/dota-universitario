#encoding: utf-8

from django.db import models

class Universidade(models.Model):
    # Nome, sigla, padrão de e-mail (@ufrj.br)
    nome = models.CharField(max_length=80)
    sigla = models.CharField(max_length=8)
    padrao_email = models.CharField(max_length=40, null=True)
    
    def __unicode__(self):
        return self.sigla
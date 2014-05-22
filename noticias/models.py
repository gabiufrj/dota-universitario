from django.db import models
from usuarios.models import Usuario

class Noticia(models.Model):
    titulo = models.CharField(max_length=40)
    autor = models.CharField(max_length=40)
    resumo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField()
    data_editado = models.DateTimeField()
    campeonato = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-data_criacao']
        

class Comentario(models.Model):
    user = models.ForeignKey(Usuario)
    conteudo = models.TextField()
    
    data_criacao = models.DateTimeField()
    data_editado = models.DateTimeField()
    
    noticia = models.ForeignKey(Noticia)
    pai = models.ForeignKey('self', null=True, blank=True)
    
    def __unicode__(self):
        return self.user + ' - ' + self.conteudo
    
    class Meta:
        ordering = ['-data_criacao']
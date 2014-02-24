from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=40)
    autor = models.CharField(max_length=40)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField()
    data_editado = models.DateTimeField()
    campeonato = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-data_criacao']
from django.db import models
from django.contrib.auth.models import User

from universidades.models import Universidade

class Usuario(models.Model):
    user = models.OneToOneField(User)
    verificado = models.BooleanField(default=False)
    universidade = models.ForeignKey(Universidade)
    
    def __unicode__(self):
        return self.user.username

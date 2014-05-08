from django.contrib import admin
from noticias.models import Noticia
from noticias.models import Comentario

admin.site.register(Noticia)
admin.site.register(Comentario)
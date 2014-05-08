#encoding:utf-8

from django import forms

from noticias.models import Noticia, Comentario
from usuarios.models import Usuario

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CriarComentarioForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Digite seu comentário...'}))
    
    def clean_texto(self):
        text = self.cleaned_data['texto']
        
        if len(text) > 0:
            return text
        else:
            raise forms.ValidationError("Comentário não pode ficar em branco")
            
            
class CriarNoticiaForm(forms.Form):
    titulo = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}))
    texto = forms.CharField(widget=SummernoteWidget(attrs={'rows': 10, 'class': 'form-control', 'placeholder': 'Digite sua notícia...'}))
    
    # validações
    def clean_titulo(self):
        text = self.cleaned_data['titulo']
        
        if len(text) > 0:
            return text
        else:
            raise forms.ValidationError("Título não pode ficar em branco")
    
    def clean_texto(self):
        text = self.cleaned_data['texto']
        
        if len(text) > 0:
            return text
        else:
            raise forms.ValidationError("Notíca não pode ficar em branco")
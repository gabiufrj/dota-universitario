#encoding:utf-8

from django import forms
from django.forms import ModelForm

from universidades.models import Universidade
from usuarios.models import Usuario

class CadastroModelForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ('user', 'universidade')

class CadastroForm(forms.Form):
    CHOICES = ()
    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        universidades_disponiveis = Universidade.objects.all()
        CHOICES = [(uni.id, uni.sigla) for uni in universidades_disponiveis]
        self.fields["universidade"] = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuário'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'senha'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario@universidade.edu.br'}))    
    universidade = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Usuario.objects.get(user__username=username)
            raise forms.ValidationError("Usuário já cadastrado!")
        except Usuario.DoesNotExist:
            return username
            
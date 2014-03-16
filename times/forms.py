#encoding:utf-8

from django import forms

from universidades.models import Universidade
from times.models import Time, Contrato
from usuarios.models import Usuario

class CriarTimeForm(forms.Form):
    CHOICES = ()
    def __init__(self, *args, **kwargs):
        super(CriarTimeForm, self).__init__(*args, **kwargs)
        universidades_disponiveis = Universidade.objects.all()
        CHOICES = [(uni.id, uni.sigla) for uni in universidades_disponiveis]
        self.fields["universidade"] = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    nome = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'time'}))
    sigla = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'T'}))
    universidade = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def clean_nome(self):
        name = self.cleaned_data['nome']
        try:
            time = Time.objects.get(nome=name)
            raise forms.ValidationError("Nome de time já usado")
        except Time.DoesNotExist:
            return name
            

class InserirMembroForm(forms.Form):
    nome = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    time_id = forms.IntegerField(widget=forms.HiddenInput())
    
    # se o usuário não existir, ou já pertencer ao time, dar erro!
    def clean(self):
        cleaned_data = super(InserirMembroForm, self).clean()
        print cleaned_data
        name = cleaned_data['nome']
        time_id = cleaned_data['time_id']
        
        # checar se usuário existe
        try:
            usuario = Usuario.objects.get(user__username=name)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("Jogador não cadastrado.")
        
        # checar se já está no time
        try:
            contrato = Contrato.objects.get(user__user__username=name, time__id=time_id)
            raise forms.ValidationError("Jogador já está no time!")
        except Contrato.DoesNotExist:
            return cleaned_data
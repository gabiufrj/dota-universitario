#encoding:utf-8

from datetime import date

from django import forms

from universidades.models import Universidade
from campeonatos.models import Campeonato, Trabalho
from usuarios.models import Usuario

class CriarCampeonatoForm(forms.Form):
    CHOICES = ()
    def __init__(self, *args, **kwargs):
        super(CriarCampeonatoForm, self).__init__(*args, **kwargs)
        universidades_disponiveis = Universidade.objects.all()
        CHOICES = [(uni.id, uni.sigla) for uni in universidades_disponiveis]
        self.fields["universidade"] = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    nome = forms.CharField(label='Nome', max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do campeonato'}))
    
    universidade = forms.ChoiceField(label='Universidade', choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    vagas = forms.CharField(label='Vagas', widget=forms.TextInput(attrs={'type':'number', 'min': '0', 'class': 'form-control'}))
    
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'style': 'resize: vertical;', 'placeholder': 'Digite a descrição do campeonato...'}))
    
    inicio_inscricoes = forms.DateField(label='Início', widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
    fim_inscricoes = forms.DateField(label='Término', widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
    
    inicio_partidas = forms.DateField(label='Início', widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
    fim_partidas = forms.DateField(label='Término', widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
    
    hora_inicio_partidas = forms.CharField(label='Horário de início', widget=forms.TextInput(attrs={'class': 'form-control timepicker'}))
    hora_fim_partidas = forms.CharField(label='Horário de término', widget=forms.TextInput(attrs={'class': 'form-control timepicker'}))


    def clean(self):
        self.cleaned_data = super(CriarCampeonatoForm, self).clean()
    
        # Valida universidade. Usuário só pode criar campeonato
        # da universidade dele =). TODO!
        uni = self.cleaned_data['universidade']
    
        # Valida nome
        name = self.cleaned_data['nome']
        try:
            camp = Campeonato.objects.get(nome=name)
            self._errors['nome'] = self.error_class([u'Nome já usado'])
            del self.cleaned_data['nome']
        except Campeonato.DoesNotExist:
            camp = 'whatever'
            
        desc = self.cleaned_data['descricao']
        if len(desc) < 15:
            self._errors['descricao'] = self.error_class([u'Mínimo 15 caracteres'])
            del self.cleaned_data['descricao']
            
        # Valida datas
        try:
            form_inicio_i = self.cleaned_data['inicio_inscricoes']
        except:
            self._errors['inicio_inscricoes'] = self.error_class([u'Data inválida'])
            del self.cleaned_data['inicio_inscricoes']
            raise forms.ValidationError('Data inválida')
            
        try:
            form_fim_i = self.cleaned_data['fim_inscricoes']
        except:
            self._errors['fim_inscricoes'] = self.error_class([u'Data inválida'])
            del self.cleaned_data['fim_inscricoes']
            raise forms.ValidationError('Data inválida')
        try:
            form_inicio_p = self.cleaned_data['inicio_partidas']
        except:
            self._errors['inicio_partidas'] = self.error_class([u'Data inválida'])
            del self.cleaned_data['inicio_partidas']
            raise forms.ValidationError('Data inválida')
        try:
            form_fim_p = self.cleaned_data['fim_partidas']
        except:
            self._errors['fim_partidas'] = self.error_class([u'Data inválida'])
            del self.cleaned_data['fim_partidas']
            raise forms.ValidationError('Data inválida')
        
        # verifica se data inicio é antes de hoje
        hoje = date.today()
        if form_inicio_i < hoje:
            self._errors['inicio_inscricoes'] = self.error_class([u'Não pode começar antes de hoje'])
            del self.cleaned_data['inicio_inscricoes']
            
        # verifica se as inscrições terminam antes do inicio
        if form_fim_i <= form_inicio_i:
            self._errors['fim_inscricoes'] = self.error_class([u'Não pode ser antes do início'])
            del self.cleaned_data['fim_inscricoes']
            
        # verifica se as partidas começam antes do fim das inscrições
        if form_fim_i >= form_inicio_p:
            self._errors['inicio_partidas'] = self.error_class([u'Deve ser depois do fim de inscrições'])
            del self.cleaned_data['inicio_partidas']
            
        # verifica se o fim da partida é antes do inicio
        if form_fim_p <= form_inicio_p:
            self._errors['fim_partidas'] = self.error_class([u'Deve ser depois do início'])
            del self.cleaned_data['fim_partidas']
        
        # valida vagas
        text = self.cleaned_data['vagas']
        try:
            vagas = int(text)
        except ValueError:
            self._errors['vagas'] = self.error_class([u'Deve ser um inteiro'])
            del self.cleaned_data['vagas']
        
        return self.cleaned_data
        
        
        
class InserirStaffForm(forms.Form):
    nome = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    role = forms.ChoiceField(choices=Trabalho.ROLE_ESCOLHAS, widget=forms.Select(attrs={'class': 'form-control'}))
    camp_id = forms.IntegerField(widget=forms.HiddenInput())    
    
    def clean(self):
        cleaned_data = super(InserirStaffForm, self).clean()
        print cleaned_data
        name = cleaned_data['nome']
        camp_id = cleaned_data['camp_id']
        
        # checar se usuário existe
        try:
            usuario = Usuario.objects.get(user__username=name)
        except Usuario.DoesNotExist:
            self._errors['nome'] = self.error_class([u'Jogador não cadastrado.'])
        
        # checar se o campeonato existe
        try:
            campeonato = Campeonato.objects.get(id=camp_id)            
        except Contrato.DoesNotExist:
            raise forms.ValidationError("Campeonato não existe, verifique url!")
        
        # checar se o usuário já não é staff do camp
        try:
            contrato = Trabalho.objects.get(campeonato__id=camp_id, usuario__user__username=name)
            self._errors['nome'] = self.error_class([u'Usuário já é staff do campeonato.'])
        except Trabalho.DoesNotExist:
            return cleaned_data
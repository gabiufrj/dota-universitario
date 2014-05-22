#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime

from campeonatos.models import Campeonato, Inscricao, Partida, Trabalho
from campeonatos.forms import CriarCampeonatoForm, InserirStaffForm
from times.models import Time, Contrato
from universidades.models import Universidade
from usuarios.models import Usuario

def todos(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))

def em_andamento(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(inicio_partidas__lte=hoje, fim_partidas__gte=hoje)
    return render(request, 'camp-andamento.html', 
                    {'lista_campeonatos': lista_campeonatos,
                    }, context_instance=RequestContext(request)
                )
    
def inscricoes_abertas(request):
    return render(request, 'camp-inscricoes-abertas.html', {},
                    context_instance=RequestContext(request)
                )
    
def terminados(request):
    hoje = datetime.date.today
    lista_campeonatos = Campeonato.objects.filter(fim_partidas__lt=hoje)
    return render(request, 'camp-terminados.html', 
                    {'lista_campeonatos': lista_campeonatos,
                    }, context_instance=RequestContext(request)
                )
    
def visualizar(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera campeonato no banco
    try:
        campeonato = Campeonato.objects.get(id=id)
    except Campeonato.DoesNotExist:
        raise Http404()
        
    # recupera inscricoes do campeonato
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    
    # recupera partidas do campeonato
    partidas = Partida.objects.filter(campeonato=campeonato)
    
    # verifica se o usuário é criador do campeonato
    criador = (request.user.username == campeonato.criador.user.username)
    
    # verifica se as inscrições estão abertas
    hoje = datetime.date.today()
    inscricoes_abertas = False
    if campeonato.fim_inscricoes >= hoje:
        if campeonato.inicio_inscricoes <= hoje:
            inscricoes_abertas = True
    
    return render(request, 'camp-visualizar.html', 
                    {
                        'campeonato': campeonato,
                        'inscricoes': inscricoes,
                        'partidas': partidas,
                        'inscricoes_abertas': inscricoes_abertas,
                        'criador': criador,
                    }, context_instance=RequestContext(request)
                )
                
@login_required()
def inscrever(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera campeonato no banco
    try:
        campeonato = Campeonato.objects.get(id=id)
    except Campeonato.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        # recupera usuário e times que ele é capitão
        contratos = Contrato.objects.filter(user__user__username=request.user.username, capitao=True)
        times = []
        for contrato in contratos:
            times.append(contrato.time)
        
        return render(request, 'camp-inscricao.html', 
                        {
                            'campeonato': campeonato,
                            'times': times,
                        }, context_instance=RequestContext(request)
                    )
    else:
        if 'time' in request.POST and request.POST['time']:
            id_time = request.POST['time']
            # pega o time selecionado
            try:
                time = Time.objects.get(id=id_time)
            except Time.DoesNotExist:
                raise Http404()
            
            # cria inscrição
            inscricao, created = Inscricao.objects.get_or_create(time=time, campeonato=campeonato)
            return redirect('/')
        else:
            raise Http404()



            
def adiciona_staff_backend(data):
    try:
        form_nome = data['nome']
        form_camp_id = data['camp_id']
        form_role = data['role']
    except:
        return False
        
    # confere se o campeonato existe
    try:
        campeonato = Campeonato.objects.get(id=form_camp_id)
    except Campeonato.DoesNotExist:
        return False
        
    # confere se o usuário existe mesmo
    try:
        usuario = Usuario.objects.get(user__username=form_nome)
    except Usuario.DoesNotExist:
        return False
        
    # cria objeto
    trabalho_novo, created = Trabalho.objects.get_or_create(campeonato=campeonato, usuario=usuario, papel=form_role)
    return True

        
@login_required()
def adiciona_staff(request, id):
    if request.method == 'GET':
        form = InserirStaffForm(initial={'camp_id': id})
    else:
        form = InserirStaffForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if adiciona_staff_backend(form_data):
                messages.success(request, 'Campeonato criado com sucesso!')
                return redirect('/campeonatos/' + id + '/')
            else:
                messages.error(request, 'Erro interno ao inserir campeonato =/. Tente mais tarde ou contate-nos sobre o erro.')
                return redirect('/campeonatos/' + id + '/')
        else:
            messages.error(request, 'Parece que há algo errado com seu formulário, confira-o e tente de novo =).')
                
    return render(request, 'camp-add-staff.html', 
                    {
                        'staff_form': form,
                    }, context_instance=RequestContext(request)
                )

            
    
def cria_campeonato(username, data):
    try:
        form_nome = data['nome']
        form_descricao = data['descricao']
        form_universidade = data['universidade']
        form_inicio_inscricoes = data['inicio_inscricoes']
        form_fim_inscricoes = data['fim_inscricoes']
        form_inicio_partidas = data['inicio_partidas']
        form_fim_partidas = data['fim_partidas']
        form_vagas = data['vagas']
    except:
        return 'dados do form inválidos'

    # Pega a universidade escolhida, pelo id
    try:
        uni = Universidade.objects.get(id=form_universidade)
    except Universidade.DoesNotExist:
        return 'universidade não existe'

    # Associa o usuario ao campeonato
    try:
        usuario = Usuario.objects.get(user__username=username)
    except Usuario.DoesNotExist:
        return 'usuário não encontrado'
        
    # Cria o campeonato
    camp_novo = Campeonato()
    camp_novo.criador = usuario
    camp_novo.nome = form_nome
    camp_novo.universidade = uni
    camp_novo.descricao = form_descricao
    camp_novo.inicio_inscricoes = form_inicio_inscricoes
    camp_novo.fim_inscricoes = form_fim_inscricoes
    camp_novo.inicio_partidas = form_inicio_partidas
    camp_novo.fim_partidas = form_fim_partidas
    camp_novo.vagas = form_vagas
    camp_novo.formato = 'RR'
    camp_novo.save()
    
    return 'sucesso'
    
@login_required()
def criar(request):
    sucesso = 0
    if request.method == 'GET':
        form = CriarCampeonatoForm()
    else:
        form = CriarCampeonatoForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            sucesso = form_data
            sucesso = cria_campeonato(request.user.username, form_data)
            if sucesso == 'sucesso':
                messages.success(request, 'Campeonato criado com sucesso!')
                return redirect('/campeonatos/todos/')
            else:
                messages.error(request, 'Erro interno ao inserir campeonato =/. Tente mais tarde ou contate-nos sobre o erro.')
                return redirect('/campeonatos/todos/')
        else:
            messages.error(request, 'Parece que há algo errado com seu formulário, confira-o e tente de novo =).')
            sucesso = 'form inválido'
                
    return render(request, 'camp-criar.html', 
                    {
                        'campeonato_form': form,
                        'sucesso': sucesso,
                    }, context_instance=RequestContext(request)
                )


# relacionados a partidas
def visualizar_partida(request, id):
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera partida no banco
    try:
        partida = Partida.objects.get(id=id)
    except Partida.DoesNotExist:
        raise Http404()
    
    return render(request, 'partida-visualizar.html', 
                    {
                        'partida': partida,
                    }, context_instance=RequestContext(request)
                )
                

@login_required()
def partida_gerar_senha(request, id):
    # recupera a partida
    # verifica se o id é realmente inteiro
    try:
        id = int(id)
    except ValueError:
        raise Http404()
        
    # recupera partida no banco
    try:
        partida = Partida.objects.get(id=id)
    except Partida.DoesNotExist:
        raise Http404()
        
    # gera senha aleatoria
    partida.senha_lobby = "senhaAleatoria"
    # salva no banco
    partida.save()
    # retorna pra página da partida
    return redirect('/partidas/' + id)
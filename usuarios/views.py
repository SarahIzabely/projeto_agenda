from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HorarioDisponivel, UsuarioAdaptado, Agendamento
from .forms import UsuarioAdaptadoCreationForm, LoginForm, PerfilForm, HorarioDisponivelForm
from django.contrib.auth.models import Group


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            
            login(request, user)
            messages.success(request, f'Cadastro realizado com sucesso! Bem-vindo, {user.username}.')
            
            # Redireciona dependendo do tipo de usuário
            if hasattr(user, 'is_professional') and user.is_professional:
                return redirect('listar_horarios')
            else:
                return redirect('listar_horarios')  # paciente vai para a listagem de horários
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UsuarioAdaptadoCreationForm()
    
    return render(request, 'usuarios/cadastrar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_professional') and request.user.is_professional:
            return redirect('listar_horarios')
        else:
            return redirect('listar_horarios')  # paciente vai para a listagem de horários
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                
                if hasattr(user, 'is_professional') and user.is_professional:
                    next_page = request.GET.get('next', 'listar_horarios')
                else:
                    next_page = request.GET.get('next', 'listar_horarios')
                return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


@login_required
def perfil_view(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
def listar_horarios(request):
    if not request.user.is_professional:
        # Paciente pode ver todos os horários disponíveis
        horarios = HorarioDisponivel.objects.all().order_by('data', 'hora_inicio')
        return render(request, 'horarios_paciente/listar_horarios.html', {'horarios': horarios})
    
    # Profissional vê apenas os seus
    horarios = HorarioDisponivel.objects.filter(profissional=request.user)
    return render(request, 'usuarios/horarios_list.html', {'horarios': horarios})


@login_required
def criar_horario(request):
    if not request.user.is_professional:
        messages.error(request, "Acesso negado. Apenas profissionais podem acessar.")
        return redirect('perfil')

    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.profissional = request.user
            horario.save()
            messages.success(request, "Horário cadastrado com sucesso!")
            return redirect('listar_horarios')
    else:
        form = HorarioDisponivelForm()

    return render(request, 'usuarios/horarios_form.html', {'form': form, 'titulo': 'Cadastrar Horário'})


@login_required
def editar_horario(request, pk):
    if not request.user.is_professional:
        messages.error(request, "Acesso negado. Apenas profissionais podem acessar.")
        return redirect('perfil')

    horario = get_object_or_404(HorarioDisponivel, pk=pk, profissional=request.user)

    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, "Horário atualizado com sucesso!")
            return redirect('listar_horarios')
    else:
        form = HorarioDisponivelForm(instance=horario)

    return render(request, 'usuarios/horarios_form.html', {'form': form, 'titulo': 'Editar Horário'})


@login_required
def deletar_horario(request, pk):
    if not request.user.is_professional:
        messages.error(request, "Acesso negado. Apenas profissionais podem acessar.")
        return redirect('perfil')

    horario = get_object_or_404(HorarioDisponivel, pk=pk, profissional=request.user)

    if request.method == 'POST':
        horario.delete()
        messages.success(request, "Horário excluído com sucesso!")
        return redirect('listar_horarios')

    return render(request, 'usuarios/horarios_confirm_delete.html', {'horario': horario})


# =========================
# Novas views para profissionais
# =========================

@login_required
def listar_profissionais(request):
    profissionais = UsuarioAdaptado.objects.filter(is_professional=True)
    context = {
        'profissionais': profissionais
    }
    return render(request, 'profissionais/lista.html', context)


@login_required
def detalhe_profissional(request, pk):
    profissional = get_object_or_404(UsuarioAdaptado, pk=pk, is_professional=True)
    context = {
        'profissional': profissional
    }
    return render(request, 'profissionais/detalhe.html', context)

@login_required
def detalhes_consulta(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)
    return render(request, 'horarios_paciente/detalhes_consulta.html', {'horario': horario})


@login_required
def confirmar_agendamento(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)

    # Evita que profissionais agendem seus próprios horários
    if request.user == horario.profissional:
        messages.error(request, "Você não pode agendar consigo mesmo.")
        return redirect('listar_horarios')

    # Cria o agendamento
    Agendamento.objects.create(
        paciente=request.user,
        profissional=horario.profissional,
        data=horario.data,
        hora_inicio=horario.hora_inicio,
        hora_fim=horario.hora_fim
    )

    # Desativa o horário (para não ficar disponível)
    horario.ativo = False
    horario.save()

    messages.success(request, "Agendamento confirmado com sucesso!")
    return redirect('listar_horarios')

@login_required
def horarios_agendados(request):
    user = request.user
    context = {}

    # Se o usuário for profissional, mostra os horários marcados com ele
    if user.groups.filter(name='profissionais').exists():
        consultas = Agendamento.objects.filter(profissional=user).order_by('-data', '-horario')
        context['titulo'] = "Horários Agendados com Você"
        context['consultas'] = consultas
        return render(request, 'horarios_paciente/horarios_agendados.html', context)

    # Se for paciente comum
    elif user.groups.filter(name='usuarios_comum').exists():
        consultas = Agendamento.objects.filter(paciente=user).order_by('-data', '-horario')
        context['titulo'] = "Seus Horários Agendados"
        context['consultas'] = consultas
        return render(request, 'horarios_paciente/horarios_agendados.html', context)

    # Caso não pertença a nenhum grupo (ou admin)
    else:
        context['consultas'] = []
        context['titulo'] = "Horários Agendados"
        return render(request, 'horarios_paciente/horarios_agendados.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .models import HorarioDisponivel, UsuarioAdaptado, Agendamento, AvisoCancelamento
from .forms import UsuarioAdaptadoCreationForm, LoginForm, PerfilForm, HorarioDisponivelForm
from django.contrib.auth.models import Group


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            grupo_simples, _ = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)

            login(request, user)
            messages.success(request, f'Cadastro realizado com sucesso! Bem-vindo, {user.username}.')
            return redirect('listar_horarios')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UsuarioAdaptadoCreationForm()

    return render(request, 'usuarios/cadastrar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('listar_horarios')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                return redirect('listar_horarios')
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
    # ---------- CONFIGURAÇÃO DOS FILTROS ----------
    profissional_id = request.GET.get("profissional")
    data = request.GET.get("data")
    status = request.GET.get("status")

    # ---------- PACIENTE ----------
    if not request.user.is_professional:
        horarios = HorarioDisponivel.objects.filter(ativo=True).order_by("data", "hora_inicio")

        # Filtro por profissional
        if profissional_id:
            horarios = horarios.filter(profissional_id=profissional_id)

        # Filtro por data
        if data:
            horarios = horarios.filter(data=data)

        # Paginação
        paginator = Paginator(horarios, 9)
        page_number = request.GET.get("page")
        horarios = paginator.get_page(page_number)

        profissionais = UsuarioAdaptado.objects.filter(is_professional=True).order_by("first_name")

        context = {
            "horarios": horarios,
            "profissionais": profissionais,
        }
        return render(request, "horarios_paciente/listar_horarios.html", context)

    # ---------- PROFISSIONAL ----------
    else:
        horarios = HorarioDisponivel.objects.filter(profissional=request.user).order_by("data", "hora_inicio")

        # Filtro por data
        if data:
            horarios = horarios.filter(data=data)

        # Filtro por status (ativo/inativo)
        if status == "ativo":
            horarios = horarios.filter(ativo=True)
        elif status == "inativo":
            horarios = horarios.filter(ativo=False)

        # Paginação
        paginator = Paginator(horarios, 9)
        page_number = request.GET.get("page")
        horarios = paginator.get_page(page_number)

        context = {
            "horarios": horarios,
        }
        return render(request, "horarios_profissionais/listar_horarios.html", context)
    

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
    """Permite que o profissional exclua um horário e, caso haja um agendamento,
    ele é removido e o paciente é notificado automaticamente."""
    horario = get_object_or_404(HorarioDisponivel, pk=pk, profissional=request.user)

    if request.method == 'POST':
        # procura se há agendamento vinculado a esse horário
        agendamento_existente = Agendamento.objects.filter(
            profissional=request.user,
            data=horario.data,
            hora_inicio=horario.hora_inicio,
            hora_fim=horario.hora_fim
        ).first()

        if agendamento_existente:
            # cria aviso para o paciente
            AvisoCancelamento.objects.create(
                paciente=agendamento_existente.paciente,
                profissional=request.user,
                data=horario.data,
                hora_inicio=horario.hora_inicio,
                mensagem=(
                    f"O horário das {horario.hora_inicio.strftime('%H:%M')} "
                    f"no dia {horario.data.strftime('%d/%m/%Y')} com "
                    f"{request.user.get_full_name()} foi cancelado."
                ),
                lido=False
            )

            # remove o agendamento
            agendamento_existente.delete()

        # exclui o horário
        horario.delete()

        messages.success(
            request,
            "Horário excluído com sucesso! Se havia uma consulta agendada, o paciente foi notificado."
        )
        return redirect('listar_horarios')

    return render(request, 'usuarios/horarios_confirm_delete.html', {'horario': horario})


@login_required
def listar_profissionais(request):
    profissionais = UsuarioAdaptado.objects.filter(is_professional=True)
    return render(request, 'profissionais/lista.html', {'profissionais': profissionais})


@login_required
def detalhe_profissional(request, pk):
    profissional = get_object_or_404(UsuarioAdaptado, pk=pk, is_professional=True)
    return render(request, 'profissionais/detalhe.html', {'profissional': profissional})


@login_required
def detalhes_consulta(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)
    return render(request, 'horarios_paciente/detalhes_consulta.html', {'horario': horario})


@login_required
def confirmar_agendamento(request, pk):
    """Confirma um agendamento e associa paciente e profissional."""
    horario = get_object_or_404(HorarioDisponivel, pk=pk, ativo=True)

    # Impede o profissional de agendar consigo mesmo
    if request.user == horario.profissional:
        messages.error(request, "Você não pode agendar um horário consigo mesmo.")
        return redirect('listar_horarios')

    # Impede o usuário de agendar um horário já agendado
    if Agendamento.objects.filter(
        profissional=horario.profissional,
        data=horario.data,
        hora_inicio=horario.hora_inicio,
        hora_fim=horario.hora_fim
    ).exists():
        messages.warning(request, "Este horário já foi agendado por outra pessoa.")
        return redirect('listar_horarios')

    # Cria o agendamento
    Agendamento.objects.create(
        paciente=request.user,
        profissional=horario.profissional,
        data=horario.data,
        hora_inicio=horario.hora_inicio,
        hora_fim=horario.hora_fim,
        criado_em=timezone.now()
    )

    # Marca o horário como indisponível
    horario.ativo = False
    horario.save()

    messages.success(request, "Agendamento confirmado com sucesso!")
    return redirect('horarios_agendados')

@login_required
def cancelar_agendamento(request, pk):
    """Permite que o paciente cancele um agendamento."""
    agendamento = get_object_or_404(Agendamento, pk=pk, paciente=request.user)

    # Reativa o horário correspondente
    horario = HorarioDisponivel.objects.filter(
        profissional=agendamento.profissional,
        data=agendamento.data,
        hora_inicio=agendamento.hora_inicio,
        hora_fim=agendamento.hora_fim
    ).first()

    if horario:
        horario.ativo = True
        horario.save()

    agendamento.delete()
    messages.success(request, "Agendamento cancelado com sucesso!")
    return redirect('horarios_agendados')


# HORÁRIOS AGENDADOS (ambos os perfis)

@login_required
def horarios_agendados(request):
    """Lista todos os horários agendados pelo usuário logado (somente os não concluídos)."""
    if request.user.is_professional:
        consultas = Agendamento.objects.filter(
            profissional=request.user,
            concluida=False
        ).order_by('data', 'hora_inicio')
        titulo = "Meus Agendamentos com Pacientes"
        aviso = None  # profissionais não recebem avisos
    else:
        consultas = Agendamento.objects.filter(
            paciente=request.user,
            concluida=False
        ).order_by('data', 'hora_inicio')
        titulo = "Meus Horários Agendados"

        # Verifica se há algum aviso de cancelamento não lido
        aviso = AvisoCancelamento.objects.filter(paciente=request.user, lido=False).order_by('-data', '-hora_inicio').first()

    return render(
        request,
        'horarios_paciente/horarios_agendados.html',
        {
            'consultas': consultas,
            'titulo': titulo,
            'aviso': aviso
        }
    )

# HORÁRIOS ARQUIVADOS (ambos os perfis)

@login_required
def horarios_arquivados(request):
    """Lista os agendamentos concluídos (arquivados) para o usuário logado."""
    if request.user.is_professional:
        consultas_concluidas = Agendamento.objects.filter(
            profissional=request.user, concluida=True
        ).order_by('-data', '-hora_inicio')
    else:
        consultas_concluidas = Agendamento.objects.filter(
            paciente=request.user, concluida=True
        ).order_by('-data', '-hora_inicio')

    return render(request, 'horarios_paciente/horarios_arquivados.html', {
        'consultas': consultas_concluidas
    })


# CONCLUIR CONSULTA (ambos podem)

from django.db.models import Q

@login_required
def concluir_consulta(request, pk):
    """Marca uma consulta como concluída (paciente ou profissional)."""
    agendamento = get_object_or_404(
        Agendamento.objects.filter(
            Q(paciente=request.user) | Q(profissional=request.user)
        ),
        pk=pk
    )

    agendamento.concluida = True
    agendamento.save()

    messages.success(request, "Consulta marcada como concluída com sucesso!")
    return redirect('horarios_agendados')


@login_required
def desmarcar_conclusao(request, pk):
    """Desmarca uma consulta como concluída e a retorna aos horários agendados."""
    agendamento = get_object_or_404(
        Agendamento.objects.filter(
            Q(paciente=request.user) | Q(profissional=request.user)
        ),
        pk=pk
    )

    agendamento.concluida = False
    agendamento.save()

    messages.success(request, "Consulta marcada novamente como pendente.")
    return redirect('horarios_arquivados')


# AVISOS DE CANCELAMENTO (paciente)

@login_required
def avisos_cancelamento(request):
    """Lista os avisos de cancelamento recebidos pelo paciente."""
    avisos = AvisoCancelamento.objects.filter(paciente=request.user).order_by('-data', '-hora_inicio')
    return render(request, 'horarios_paciente/avisos_cancelamento.html', {'avisos': avisos})

@login_required
def marcar_aviso_lido(request, pk=None):
    """Marca os avisos como lidos (chamado automaticamente quando o paciente fecha o popup)."""
    AvisoCancelamento.objects.filter(paciente=request.user, lido=False).update(lido=True)
    return redirect('horarios_agendados')
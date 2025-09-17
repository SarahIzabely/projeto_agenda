from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Availability, Professional, Appointment, Paciente
import re, datetime


# Função para validar CPF
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)  # remove pontos e traços
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma2 * 10 % 11) % 10
    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])


# Cadastro do paciente
def cadastro_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar_senha')
        foto = request.FILES.get('foto')

        # CPF inválido
        if not validar_cpf(cpf):
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'CPF inválido.',
                'nome': nome,
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'email': email,
                'whatsapp': whatsapp,
                'senha': senha,
                'foto': foto
            })

        # CPF ou e-mail já existem
        if Paciente.objects.filter(cpf_paciente=cpf).exists():
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'CPF já cadastrado.',
                'nome': nome,
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'email': email,
                'whatsapp': whatsapp,
                'senha': senha,
                'foto': foto
            })

        if Paciente.objects.filter(email=email).exists():
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'E-mail já cadastrado.',
                'nome': nome,
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'email': email,
                'whatsapp': whatsapp,
                'senha': senha,
                'foto': foto
            })

        # Senhas não coincidem
        if senha != confirmar:
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'As senhas não coincidem.',
                'nome': nome,
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'email': email,
                'whatsapp': whatsapp,
                'senha': senha,
                'foto': foto
            })

        # Criar paciente
        paciente = Paciente.objects.create(
            nome=nome,
            cpf_paciente=cpf,
            data_nascimento=data_nascimento,
            email=email,
            whatsapp_paciente=whatsapp,
            senha=senha,
            foto=foto
        )

        request.session['paciente_id'] = paciente.id
        return redirect('dashboard')

    return render(request, 'agenda/cadastro_paciente.html')


# Função para pegar paciente da sessão
def _get_paciente_from_session(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return None
    try:
        return Paciente.objects.get(id=paciente_id)
    except Paciente.DoesNotExist:
        return None


# Login do paciente
def login_paciente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        paciente = Paciente.objects.filter(email=email, senha=senha).first()
        if paciente:
            request.session['paciente_id'] = paciente.id
            return redirect('dashboard')
        else:
            return render(request, 'agenda/login_paciente.html', {'erro': 'E-mail ou senha incorretos.'})
    return render(request, 'agenda/login_paciente.html')


# Dashboard do paciente
def dashboard(request):
    paciente = _get_paciente_from_session(request)
    if not paciente:
        return redirect('login_paciente')

    hoje = datetime.date.today()
    availabilities = Availability.objects.filter(disponivel=True, data__gte=hoje).select_related('profissional')
    professionals = Professional.objects.filter(ativo=True).order_by('nome')

    context = {
        'paciente': paciente,
        'availabilities': availabilities,
        'professionals': professionals,
    }
    return render(request, 'agenda/dashboard.html', context)


# Listagem de profissionais
def profissionais_view(request):
    paciente = _get_paciente_from_session(request)
    if not paciente:
        return redirect('login_paciente')

    pros = Professional.objects.filter(ativo=True).order_by('nome')
    return render(request, 'agenda/profissionais.html', {'paciente': paciente, 'professionals': pros})


# Agendamento de consulta
def book_appointment(request):
    paciente = _get_paciente_from_session(request)
    if not paciente:
        return redirect('login_paciente')

    if request.method == 'POST':
        availability_id = request.POST.get('availability_id')
        availability = get_object_or_404(Availability, id=availability_id, disponivel=True)
        Appointment.objects.create(paciente=paciente, disponibilidade=availability)
        availability.disponivel = False
        availability.save()
        return redirect('dashboard')

    return redirect('dashboard')

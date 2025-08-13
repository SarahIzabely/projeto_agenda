from django.shortcuts import render
from django.http  import HttpResponse
from django.shortcuts import render, redirect
from .models import Paciente
import re

def cadastro_paciente(request):
    return render(request, 'clinica/cadastro_paciente.html')

def cadastro_profissional(request):
    return render(request, 'clinica/cadastro_profissional.html')

def cadastro_administrador(request):
    return render(request, 'clinica/cadastro_administrador.html')

def login_paciente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        # Aqui você faria a autenticação (depois a gente implementa com User)
        # Se for válido, redireciona para a tela de agendamento:
        return redirect('agendamento_paciente')
    return render(request, 'agenda/login_paciente.html')

def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)  # remove pontos e traços

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma2 * 10 % 11) % 10

    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])

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
                'nome_paciente': nome,
                'cpf_paciente': cpf,
                'data_nascimento': data_nascimento,
                'email_paciente': email,
                'whatsapp_paciente': whatsapp,
                'senha_paciente': senha,
                'foto': foto
            })

        # CPF ou e-mail já existem
        if Paciente.objects.filter(cpf_paciente=cpf).exists():
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'CPF já cadastrado.',
                'nome_paciente': nome,
                'cpf_paciente': cpf,
                'data_nascimento': data_nascimento,
                'email_paciente': email,
                'whatsapp_paciente': whatsapp,
                'senha_paciente': senha,
                'foto': foto
            })

        if Paciente.objects.filter(email_paciente=email).exists():
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'E-mail já cadastrado.',
                'nome_paciente': nome,
                'cpf_paciente': cpf,
                'data_nascimento': data_nascimento,
                'email_paciente': email,
                'whatsapp_paciente': whatsapp,
                'senha_paciente': senha,
                'foto': foto
            })

        if senha != confirmar:
            return render(request, 'agenda/cadastro_paciente.html', {
                'erro': 'As senhas não coincidem.',
                'nome_paciente': nome,
                'cpf_paciente': cpf,
                'data_nascimento': data_nascimento,
                'email_paciente': email,
                'whatsapp_paciente': whatsapp,
                'senha_paciente': senha,
                'foto': foto
            })

        paciente = Paciente.objects.create(
            nome_paciente=nome,
            cpf_paciente=cpf,
            data_nascimento=data_nascimento,
            email_paciente=email,
            whatsapp_paciente=whatsapp,
            senha_paciente=senha,
            foto=foto
        )

        return redirect('agendamento_paciente')

    return render(request, 'agenda/cadastro_paciente.html')
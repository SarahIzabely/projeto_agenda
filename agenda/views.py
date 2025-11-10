from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import HorarioDisponivel
from .forms import HorarioDisponivelForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# 🏠 Redireciona a home (/) para a listagem de horários
def home(request):
    return redirect('listar_horarios')


# 👥 Lista horários disponíveis (para pacientes)
def listar_horarios(request):
    horarios = HorarioDisponivel.objects.filter(ativo=True).order_by('data', 'hora_inicio')
    return render(request, 'horarios_paciente/listar_horarios.html', {'horarios': horarios})


# ➕ Profissional cria horário
@login_required
def criar_horario(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.profissional = request.user  # associa o usuário logado
            horario.save()
            messages.success(request, 'Horário criado com sucesso!')
            return redirect('listar_horarios')
        else:
            messages.error(request, 'Erro ao salvar o horário. Verifique os campos.')
    else:
        form = HorarioDisponivelForm()
    return render(request, 'horarios_profissional/form_horario.html', {'form': form, 'titulo': 'Criar Horário'})


# ✏️ Profissional edita horário
@login_required
def editar_horario(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)
    if request.user != horario.profissional:
        messages.error(request, 'Você não tem permissão para editar este horário.')
        return redirect('listar_horarios')

    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário atualizado com sucesso!')
            return redirect('listar_horarios')
    else:
        form = HorarioDisponivelForm(instance=horario)
    return render(request, 'horarios_profissional/form_horario.html', {'form': form, 'titulo': 'Editar Horário'})


# ❌ Profissional deleta horário
@login_required
def deletar_horario(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)
    if request.user != horario.profissional:
        messages.error(request, 'Você não tem permissão para deletar este horário.')
        return redirect('listar_horarios')

    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horário deletado com sucesso!')
        return redirect('listar_horarios')
    return render(request, 'horarios_profissional/confirmar_delete.html', {'horario': horario})


# 📅 Detalhes da consulta (nova tela)
@login_required
def detalhes_consulta(request, pk):
    horario = get_object_or_404(HorarioDisponivel, pk=pk)
    return render(request, 'horarios_paciente/detalhes_consulta.html', {'horario': horario})


# 🧠 View de depuração — mostra todos os horários do banco (para checar IDs)
def ver_horarios_debug(request):
    horarios = HorarioDisponivel.objects.all()
    if not horarios.exists():
        return HttpResponse("<h3>Nenhum horário cadastrado no banco.</h3>")
    
    html = "<h2>Horários Cadastrados</h2><ul>"
    for h in horarios:
        html += f"<li>ID: {h.id} | Profissional: {h.profissional.get_full_name()} | Data: {h.data} | Hora: {h.hora_inicio}</li>"
    html += "</ul>"
    return HttpResponse(html)

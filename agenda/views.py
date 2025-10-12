from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import HorarioDisponivel
from .forms import HorarioDisponivelForm
from django.contrib.auth.decorators import login_required

# Redireciona a home (/) para a listagem de horários
def home(request):
    return redirect('listar_horarios')

# Lista horários para pacientes
def listar_horarios(request):
    horarios = HorarioDisponivel.objects.all().order_by('data', 'hora_inicio')
    return render(request, 'horarios_paciente/listar_horarios.html', {'horarios': horarios})

# Profissional cria horário
@login_required
def criar_horario(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário criado com sucesso!')
            return redirect('listar_horarios')
    else:
        form = HorarioDisponivelForm()
    return render(request, 'horarios_profissional/form_horario.html', {'form': form, 'titulo': 'Criar Horário'})

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

from django.contrib import admin
from .models import Administrador, Paciente, Profissional, Agendamento, Horario_disponivel

# Registrando os modelos no admin
admin.site.register(Administrador)
admin.site.register(Paciente)
admin.site.register(Profissional)
admin.site.register(Agendamento)
admin.site.register(Horario_disponivel)

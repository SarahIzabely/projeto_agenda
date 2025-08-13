from django.contrib import admin
from .models import Administrador, Paciente, Profissional, Agendamento, Consulta, Receita_medica, Horario_disponivel, Comprovante_pagamento, Mensagem_WPP


admin.site.register(Paciente)
admin.site.register(Profissional)
admin.site.register(Administrador)
admin.site.register(Consulta)
admin.site.register(Comprovante_pagamento)
admin.site.register(Horario_disponivel)
admin.site.register(Receita_medica)
admin.site.register(Agendamento)
admin.site.register(Mensagem_WPP)

# Register your models here.

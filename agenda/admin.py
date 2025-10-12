from django.contrib import admin
from .models import HorarioDisponivel

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ('id', 'profissional', 'data', 'hora_inicio', 'hora_fim')
    list_filter = ('data', 'profissional')
    search_fields = ('profissional__username',)
    date_hierarchy = 'data'

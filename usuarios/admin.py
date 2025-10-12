from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAdaptado

@admin.register(UsuarioAdaptado)
class UsuarioAdaptadoAdmin(UserAdmin):
    model = UsuarioAdaptado
    list_display = ['username', 'email', 'cpf', 'is_professional', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_professional', 'groups']
    search_fields = ['username', 'email', 'cpf', 'nome_cidade']

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'cpf', 'nome_cidade', 'endereco', 'nome_bairro',
                'data_nascimento', 'foto_perfil', 'is_professional'
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'cpf', 'nome_cidade', 'endereco', 'nome_bairro',
                'data_nascimento', 'foto_perfil', 'is_professional'
            )
        }),
    )

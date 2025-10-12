from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioAdaptado, HorarioDisponivel

class UsuarioAdaptadoCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioAdaptado
        fields = [
            'username', 'email', 'cpf', 'nome_cidade', 'data_nascimento',
            'endereco', 'nome_bairro', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF (apenas números)'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nome de usuário'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }))

class PerfilForm(forms.ModelForm):
    """Formulário para editar perfil do usuário"""
    class Meta:
        model = UsuarioAdaptado
        fields = [
            'first_name', 'last_name', 'email', 'foto_perfil',
            'nome_cidade', 'data_nascimento', 'endereco', 'nome_bairro',
            'especializacao', 'crm', 'telefone_contato', 'email_profissional', 'biografia'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'especializacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialização'}),
            'crm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CRM'}),
            'telefone_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone de Contato'}),
            'email_profissional': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail Profissional'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve biografia'}),
        }
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'foto_perfil': 'Foto de Perfil',
            'nome_cidade': 'Cidade',
            'data_nascimento': 'Data de Nascimento',
            'endereco': 'Endereço',
            'nome_bairro': 'Bairro',
            'especializacao': 'Especialização',
            'crm': 'CRM',
            'telefone_contato': 'Telefone de Contato',
            'email_profissional': 'E-mail Profissional',
            'biografia': 'Biografia',
        }


class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = ['data', 'hora_inicio', 'hora_fim', 'ativo']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'data': 'Data do Atendimento',
            'hora_inicio': 'Início',
            'hora_fim': 'Fim',
            'ativo': 'Ativo',
        }
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

class UsuarioAdaptado(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    nome_cidade = models.CharField(max_length=100, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    nome_bairro = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, verbose_name="Foto de Perfil")
    is_professional = models.BooleanField(default=False)

    # Campos profissionais
    especializacao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialização")
    crm = models.CharField(max_length=50, blank=True, null=True, verbose_name="CRM")
    telefone_contato = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone de Contato")
    email_profissional = models.EmailField(blank=True, null=True, verbose_name="E-mail Profissional")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")

    def __str__(self):
        return f"{self.username} - {self.cpf}"

    def is_gerente(self):
        return self.groups.filter(name="GERENTE").exists()

    def is_user_simples(self):
        return self.groups.filter(name="USUARIO_SIMPLES").exists()


class HorarioDisponivel(models.Model):
    profissional = models.ForeignKey(
        UsuarioAdaptado, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_professional': True},
        related_name='usuarios_horarios'
    )
    data = models.DateField(verbose_name="Data do Atendimento")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    ativo = models.BooleanField(default=True, verbose_name="Disponível")

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.profissional.username} - {self.data} {self.hora_inicio} às {self.hora_fim}"
    
class Agendamento(models.Model):
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agendamentos_paciente'
    )
    profissional = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agendamentos_profissional'
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    criado_em = models.DateTimeField(default=timezone.now)
    concluida = models.BooleanField(default=False, verbose_name="Consulta Concluída")  # 🔵 novo campo

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.paciente.username} com {self.profissional.username} em {self.data}"

class AvisoCancelamento(models.Model):
    paciente = models.ForeignKey(UsuarioAdaptado, on_delete=models.CASCADE)
    profissional = models.ForeignKey(UsuarioAdaptado, on_delete=models.CASCADE, related_name='avisos_cancelamento')
    data = models.DateField()
    hora_inicio = models.TimeField()
    mensagem = models.CharField(max_length=255)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"Aviso para {self.paciente} - {self.data} {self.hora_inicio}"

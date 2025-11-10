from django.db import models
from django.conf import settings

class HorarioDisponivel(models.Model):
    profissional = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa o UsuarioAdaptado
        on_delete=models.CASCADE,
        limit_choices_to={'is_professional': True},
        related_name='horarios_disponiveis'
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

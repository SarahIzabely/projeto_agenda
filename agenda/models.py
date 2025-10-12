from django.db import models
from django.conf import settings

class HorarioDisponivel(models.Model):
    profissional = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='horarios_disponiveis'
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.profissional} - {self.data} {self.hora_inicio} às {self.hora_fim}"

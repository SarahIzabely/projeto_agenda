from django.db import models


class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Profissional(models.Model):
    nome_profissional = models.CharField(max_length=100)
    email_profissional = models.EmailField()
    whatsapp_profissional = models.CharField(max_length=30)
    senha_profissional = models.CharField(max_length=30)
    cpf_profissional = models.CharField(max_length=30)
    data_nascimento = models.DateField()
    especializacoes = models.CharField(max_length=200)
    crm = models.CharField(max_length=30, null=True)
    status_aprovacao = models.BooleanField() 
    foto_profissional = models.ImageField(upload_to='pacientes/fotos/', blank=True, null=True)
    #verificar tipo

    def __str__(self):
        return self.nome_profissional

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    whatsapp_paciente = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    cpf_paciente = models.CharField(max_length=30)
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to='pacientes/fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome_paciente

class Agendamento(models.Model):
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profissional_id = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    forma_pagamento = models.CharField(max_length=100) #alterar, colocar caixinhas pra marcar 
    status_pagamento = models.CharField(max_length=100) #alterar, colocar caixinhas pra marcar 
    status_agendamento = models.CharField(max_length=100) #alterar, colocar caixinhas pra marcar

    def __str__(self):
        return self.data_hora 

class Horario_disponivel(models.Model):
    profissional_id = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    Data = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()

    def __str__(self):
        return self.Data, self.hora_inicio




class Professional(models.Model):
    nome = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='profissionais/fotos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"

class Availability(models.Model):
    profissional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='availabilities')
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data', 'hora']
        unique_together = ('profissional', 'data', 'hora')  # evita duplicados

    def __str__(self):
        return f"{self.profissional.nome} — {self.data} {self.hora}"

class Appointment(models.Model):
    paciente = models.ForeignKey('agenda.Paciente', on_delete=models.CASCADE, related_name='appointments')
    disponibilidade = models.ForeignKey(Availability, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('confirmada','Confirmada'),
        ('cancelada','Cancelada'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmada')

    def __str__(self):
        return f"{self.paciente.nome} — {self.disponibilidade}"

# Create your models here.

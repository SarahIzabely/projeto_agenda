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
    status_aprovacao = models.BooleanField()  #verificar tipo

    def __str__(self):
        return self.nome_profissional

class Paciente(models.Model):
    nome_paciente = models.CharField(max_length=200)
    email_paciente = models.EmailField()
    whatsapp_paciente = models.CharField(max_length=30)
    senha_paciente = models.CharField(max_length=30)
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

class Comprovante_pagamento(models.Model):
    tipo_agendamento = models.CharField(max_length=100) #alterar isso
    agendamento_id = models.ForeignKey(Agendamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_agendamento

class Consulta(models.Model):
    agendamento_id = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=100)
    prescricao = models.CharField(max_length=100)
    observacoes_consulta = models.CharField(max_length=100)

    def __str__(self):
        return self.observacoes_consulta

class Receita_medica(models.Model):
    consulta_id = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=100) #mudar, tem q herdar
    prescricao = models.CharField(max_length=100) #mudar, tem q herdar

    def __str__(self):
        return self.diagnostico, self.prescricao

class Mensagem_WPP(models.Model):
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_mensagem = models.CharField(max_length=100) #alterar, selecionar caixinha
    texto = models.CharField(max_length=100)
    data_envio = models.DateTimeField()

    def __str__(self):
        return self.tipo_mensagem



# Create your models here.

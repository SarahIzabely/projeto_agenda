from django import forms
from .models import HorarioDisponivel

class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        # ⚠️ Removemos 'profissional' daqui, pois ele é preenchido automaticamente pelo usuário logado
        fields = ['data', 'hora_inicio', 'hora_fim']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

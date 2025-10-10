from django import forms
from django.forms import ModelForm
from veiculo.models import Veiculo

class FormularioVeiculo(ModelForm):
    """
    Formulário para o modelo Veículo.
    """
    class Meta:
        model = Veiculo
        exclude = ['usuario'] 
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'cor': forms.Select(attrs={'class': 'form-select'}),
            'combustivel': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
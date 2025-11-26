from django import forms
from django.forms import ModelForm
from tenis.models import Tenis

class FormularioTenis(ModelForm):
    """
    Formulário para o modelo Tênis.
    """
    class Meta:
        model = Tenis
        exclude = ['usuario'] 
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tamanho': forms.NumberInput(attrs={'class': 'form-control'}),
            'cor': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'tamanho': 'Tamanho',
            'cor': 'Cor',
            'tipo': 'Tipo',
            'foto': 'Foto',
        }
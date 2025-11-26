from django import forms
from .models import Anuncio

class FormularioAnuncio(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['tenis', 'titulo', 'descricao', 'preco']
        exclude = ['usuario']  
        widgets = {
            'tenis': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tenis': 'Tênis',
            'titulo': 'Título',
            'descricao': 'Descrição',
            'preco': 'Preço',
        }
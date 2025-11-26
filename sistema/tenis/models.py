from django.db import models
from django.contrib.auth.models import User
from tenis.const import OPCOES_MARCAS, OPCOES_CORES, OPCOES_TIPO
from datetime import datetime

class Tenis(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    tamanho = models.IntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_CORES)
    tipo = models.SmallIntegerField(choices=OPCOES_TIPO)
    foto = models.ImageField(blank=True, null=True, upload_to='tenis/fotos')

    def __str__(self):
        return f"{self.get_marca_display()} {self.modelo} (Tam. {self.tamanho})"

    @property
    def tamanho_grande(self):
        return self.tamanho >= 42
    
    def get_categoria_tamanho(self):
        if self.tamanho < 35:
            return "Infantil"
        elif self.tamanho < 40:
            return "Feminino"
        else:
            return "Masculino"
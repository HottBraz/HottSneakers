from django.db import models
from django.contrib.auth.models import User
from veiculo.const import OPCOES_MARCAS, OPCOES_CORES, OPCOES_COMBUSTIVEL
from datetime import datetime

class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_CORES)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEL)
    foto = models.ImageField(blank=True, null=True, upload_to='veiculo/fotos')

    def __str__(self):
        return f"{self.get_marca_display()} {self.modelo} ({self.ano})"

    @property
    def veiculo_novo(self):
        return self.ano == datetime.now().year
    
    def anos_de_uso(self):
        return datetime.now().year - self.ano
from django.db import models
from veiculo.consts import OPCOES_MARCAS, OPCOES_COR, OPCOES_COMBUSTIVEL

# Create your models here.
class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True)
    ano = models.SmallIntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_COR)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEL)
    

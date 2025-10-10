from django.db import models
from django.contrib.auth.models import User
from veiculo.models import Veiculo

class Anuncio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="anuncios")
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="anuncios")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.veiculo}"
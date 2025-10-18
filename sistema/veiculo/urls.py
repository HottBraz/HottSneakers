from django.urls import path
from veiculo.views import *

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculo.as_view(), name='criar-veiculo')
]
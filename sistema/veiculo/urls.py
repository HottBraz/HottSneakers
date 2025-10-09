from django.urls import path
from veiculo.views import *

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('cadastrar/', CadastrarVeiculo.as_view(), name='cadastrar-veiculo'),

    path('fotos/<str:arquivo>/', FotoVeiculo.as_view(), name='foto-veiculo'),
]
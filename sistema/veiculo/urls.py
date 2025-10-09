from django.urls import path
from veiculo.views import *

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('cadastrar/', CadastrarVeiculo.as_view(), name='cadastrar-veiculo'),
    path('editar/<int:pk>/', EditarVeiculo.as_view(), name='editar-veiculo'),
    path('fotos/<str:arquivo>/', FotoVeiculo.as_view(), name='foto-veiculo'),
    path('excluir/<int:pk>/', ExcluirVeiculo.as_view(), name='excluir-veiculo'),
]
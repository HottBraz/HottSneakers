from django.urls import path
from anuncio.views import *

urlpatterns = [
    path('', ListarAnuncios.as_view(), name='listar-anuncios'),
    path('cadastrar/', CadastrarAnuncio.as_view(), name='cadastrar-anuncio'),
    path('editar/<int:pk>/', EditarAnuncio.as_view(), name='editar-anuncio'),
    path('excluir/<int:pk>/', ExcluirAnuncio.as_view(), name='excluir-anuncio'),
    path('<int:pk>/', DetalhesAnuncio.as_view(), name='detalhes-anuncio'),
]

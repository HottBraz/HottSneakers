from django.urls import path
from tenis.views import *

urlpatterns = [
    path('', ListarTenis.as_view(), name='listar-tenis'),
    path('cadastrar/', CadastrarTenis.as_view(), name='cadastrar-tenis'),
    path('editar/<int:pk>/', EditarTenis.as_view(), name='editar-tenis'),
    path('fotos/<str:arquivo>/', FotoTenis.as_view(), name='foto-tenis'),
    path('excluir/<int:pk>/', ExcluirTenis.as_view(), name='excluir-tenis'),

    path('api/listar/', APIListarTenis.as_view(), name='api-listar-tenis'),
    path('api/criar/', APICriarTenis.as_view(), name='api-criar-tenis'),
    path('api/editar/<int:pk>/', APIEditarTenis.as_view(), name='api-editar-tenis'),
    path('api/deletar/<int:pk>/', APIExcluirTenis.as_view(), name='api-deletar-tenis'),
]
from django.contrib import admin
from .models import Anuncio

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tenis', 'preco', 'data_criacao', 'data_atualizacao')
    search_fields = ('titulo', 'descricao', 'usuario__username', 'tenis__modelo')
from django.contrib import admin
from .models import Tenis

@admin.register(Tenis)
class TenisAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_marca_display', 'modelo', 'tamanho', 'get_cor_display', 'get_tipo_display']
    list_filter = ['marca', 'cor', 'tipo', 'tamanho']
    search_fields = ['modelo', 'tamanho']

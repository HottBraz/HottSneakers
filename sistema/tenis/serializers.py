from rest_framework import serializers
from tenis.models import Tenis

class SerializadorTenis(serializers.ModelSerializer):
    """
    Serializador para model Tenis
    """
    nome_marca = serializers.SerializerMethodField(read_only=True)
    nome_cor = serializers.SerializerMethodField(read_only=True)
    nome_tipo = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Tenis
        fields = ['id', 'marca', 'modelo', 'tamanho', 'cor', 'tipo', 'foto', 'nome_marca', 'nome_cor', 'nome_tipo']
        read_only_fields = ['nome_marca', 'nome_cor', 'nome_tipo']

    def get_nome_marca(self, instancia):
        return instancia.get_marca_display()

    def get_nome_cor(self, instancia):
        return instancia.get_cor_display()

    def get_nome_tipo(self, instancia):
        return instancia.get_tipo_display()


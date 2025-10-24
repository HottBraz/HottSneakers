from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import Http404, FileResponse
from veiculo.forms import FormularioVeiculo
from veiculo.models import Veiculo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView
from veiculo.serializers import SerializadorVeiculo
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class ListarVeiculos(LoginRequiredMixin, ListView):
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/listar.html'

    def get_queryset(self):
        veiculos = Veiculo.objects.all()
        for veiculo in veiculos:
            veiculo.form = FormularioVeiculo(instance=veiculo)
        return veiculos
    
class CadastrarVeiculo(LoginRequiredMixin, CreateView):
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/cadastrar.html'
    success_url = reverse_lazy('listar-veiculos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Associa o usuário autenticado
        return super().form_valid(form)

class FotoVeiculo(LoginRequiredMixin, ListView):

    def get(self, request, arquivo):
        try:
            veiculo = Veiculo.objects.get(foto=f'veiculo/fotos/{arquivo}')
            return FileResponse(veiculo.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada.")
        except Exception as e:
            raise e
        
class EditarVeiculo(LoginRequiredMixin, UpdateView):
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/listar.html'
    success_url = reverse_lazy('listar-veiculos')

class ExcluirVeiculo(LoginRequiredMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculo/listar.html'
    success_url = reverse_lazy('listar-veiculos')

class APIListarVeiculos(ListAPIView):
    serializer_class = SerializadorVeiculo
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Veiculo.objects.all()
    

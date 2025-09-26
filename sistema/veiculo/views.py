from django.views.generic import ListView, CreateView
from veiculo.forms import FormularioVeiculo
from veiculo.models import Veiculo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ListarVeiculos(LoginRequiredMixin, ListView):
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/listar.html'

    def get_queryset(self):
        return Veiculo.objects.all()
    
class CadastrarVeiculo(LoginRequiredMixin, CreateView):
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/cadastrar.html'
    success_url = reverse_lazy('listar-veiculos')
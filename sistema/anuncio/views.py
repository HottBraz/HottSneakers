from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Anuncio
from .forms import FormularioAnuncio
from veiculo.models import Veiculo

class ListarAnuncios(LoginRequiredMixin, ListView):
    model = Anuncio
    context_object_name = 'lista_anuncios'
    template_name = 'anuncio/listar.html'

    def get_queryset(self):
        # Filtra os anúncios pelo usuário autenticado
        anuncios = Anuncio.objects.filter(usuario=self.request.user)
        for anuncio in anuncios:
            anuncio.form = FormularioAnuncio(instance=anuncio)
        return anuncios


class CadastrarAnuncio(LoginRequiredMixin, CreateView):
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/cadastrar.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_form(self):
        form = super().get_form()
        form.fields['veiculo'].queryset = Veiculo.objects.all()
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class EditarAnuncio(LoginRequiredMixin, UpdateView):
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/listar.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_queryset(self):
        # Garante que o usuário só pode editar seus próprios anúncios
        return Anuncio.objects.filter(usuario=self.request.user)

    def get_form(self):
        form = super().get_form()
        form.fields['veiculo'].queryset = Veiculo.objects.all()
        return form

class ExcluirAnuncio(LoginRequiredMixin, DeleteView):
    model = Anuncio
    template_name = 'anuncio/listar.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_queryset(self):
        # Garante que o usuário só pode excluir seus próprios anúncios
        return Anuncio.objects.filter(usuario=self.request.user)


class DetalhesAnuncio(LoginRequiredMixin, DetailView):
    model = Anuncio
    context_object_name = 'anuncio'
    template_name = 'anuncio/detalhes.html'

    def get_queryset(self):
        return Anuncio.objects.filter(usuario=self.request.user)
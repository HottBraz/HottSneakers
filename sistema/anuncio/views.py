from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Anuncio
from .forms import FormularioAnuncio
from tenis.models import Tenis

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
        form.fields['tenis'].queryset = Tenis.objects.all()
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
        form.fields['tenis'].queryset = Tenis.objects.all()
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
        # Permite visualizar qualquer anúncio (não apenas os do usuário logado)
        return Anuncio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anuncio = self.get_object()
        # Só fornece o formulário de edição se o anúncio for do usuário logado
        if anuncio.usuario == self.request.user:
            context['anuncio_form'] = FormularioAnuncio(instance=anuncio)
            context['is_owner'] = True
        else:
            context['is_owner'] = False
        return context


class ListarTodosAnuncios(LoginRequiredMixin, ListView):
    model = Anuncio
    context_object_name = 'lista_anuncios'
    template_name = 'anuncio/todos.html'

    def get_queryset(self):
        # Lista todos os anúncios de todos os usuários
        return Anuncio.objects.all().select_related('tenis', 'usuario')
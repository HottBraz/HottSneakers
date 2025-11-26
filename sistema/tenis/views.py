from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import Http404, FileResponse
from tenis.forms import FormularioTenis
from tenis.models import Tenis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from tenis.serializers import SerializadorTenis
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class ListarTenis(LoginRequiredMixin, ListView):
    model = Tenis
    context_object_name = 'lista_tenis'
    template_name = 'tenis/listar.html'

    def get_queryset(self):
        tenis_list = Tenis.objects.all()
        for tenis in tenis_list:
            tenis.form = FormularioTenis(instance=tenis)
        return tenis_list
    
class CadastrarTenis(LoginRequiredMixin, CreateView):
    model = Tenis
    form_class = FormularioTenis
    template_name = 'tenis/cadastrar.html'
    success_url = reverse_lazy('listar-tenis')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Associa o usuário autenticado
        return super().form_valid(form)

class FotoTenis(ListView):

    def get(self, request, arquivo):
        try:
            tenis = Tenis.objects.get(foto=f'tenis/fotos/{arquivo}')
            return FileResponse(tenis.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada.")
        except Exception as e:
            raise e
        
class EditarTenis(LoginRequiredMixin, UpdateView):
    model = Tenis
    form_class = FormularioTenis
    template_name = 'tenis/listar.html'
    success_url = reverse_lazy('listar-tenis')

class ExcluirTenis(LoginRequiredMixin, DeleteView):
    model = Tenis
    template_name = 'tenis/listar.html'
    success_url = reverse_lazy('listar-tenis')

class APIListarTenis(ListAPIView):
    serializer_class = SerializadorTenis
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenis.objects.all()
    
class APIExcluirTenis(DestroyAPIView):
    model = Tenis
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenis.objects.all()

class APICriarTenis(CreateAPIView):
    serializer_class = SerializadorTenis
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class APIEditarTenis(RetrieveUpdateAPIView):
    serializer_class = SerializadorTenis
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenis.objects.all()
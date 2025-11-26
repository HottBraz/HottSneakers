from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from tenis.models import *
from tenis.forms import *

class TestesModelTenis(TestCase):
    def setUp(self):
        self.instancia = Tenis.objects.create(
            marca=1,
            modelo="ABCDE",
            tamanho=42,
            cor=2,
            tipo=3
        )
    
    def test_tamanho_grande(self):
        self.assertTrue(self.instancia.tamanho_grande)
        self.instancia.tamanho = 38
        self.assertFalse(self.instancia.tamanho_grande)

    def test_categoria_tamanho(self):
        self.instancia.tamanho = 30
        self.assertEqual(self.instancia.get_categoria_tamanho(), "Infantil")
        self.instancia.tamanho = 37
        self.assertEqual(self.instancia.get_categoria_tamanho(), "Feminino")
        self.instancia.tamanho = 42
        self.assertEqual(self.instancia.get_categoria_tamanho(), "Masculino")

class TestesViewListarTenis(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.url = reverse('listar-tenis')
        Tenis(marca=1, modelo="Modelo1", tamanho=42, cor=1, tipo=1).save()
    
    def test_listar_tenis(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('lista_tenis')), 1)


class TestesViewCadastrarTenis(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.url = reverse('cadastrar-tenis')
        
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioTenis)

    def test_post(self):
        data = {
            'marca': 1,
            'modelo': 'ABCDE',
            'tamanho': 42,
            'cor': 2,
            'tipo': 3
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-tenis'))

        self.assertEqual(Tenis.objects.count(), 1)
        self.assertEqual(Tenis.objects.first().modelo, 'ABCDE')

class TestesViewEditarTenis(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.force_login(user=self.user)
        self.instancia = Tenis.objects.create(
            marca=1,
            modelo="ABCDE",
            tamanho=42,
            cor=2,
            tipo=3
        )
        self.url = reverse('editar-tenis', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Tenis)
        self.assertIsInstance(response.context.get('form'), FormularioTenis)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)
        self.assertEqual(response.context.get('object').modelo, self.instancia.modelo)

    def test_post(self):
        data = {
            'marca': 2,
            'modelo': 'FGHIJ',
            'tamanho': 40,
            'cor': 3,
            'tipo': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-tenis'))

        self.assertEqual(Tenis.objects.count(), 1)
        self.assertEqual(Tenis.objects.first().modelo, 'FGHIJ')
        self.assertEqual(Tenis.objects.first().marca, 2)
        self.assertEqual(Tenis.objects.first().pk, self.instancia.pk)

class TestesViewExcluirTenis(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.force_login(user=self.user)
        self.instancia = Tenis.objects.create(
            marca=1,
            modelo="ABCDE",
            tamanho=42,
            cor=2,
            tipo=3
        )
        self.url = reverse('excluir-tenis', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Tenis)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-tenis'))

        self.assertEqual(Tenis.objects.count(), 0)
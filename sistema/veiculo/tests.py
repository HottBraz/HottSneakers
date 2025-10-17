from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from veiculo.models import *
from veiculo.forms import *

class TestesModelVeiculo(TestCase):
    def setUp(self):
        self.instancia = Veiculo.objects.create(
            marca=1,
            modelo="ABCDE",
            ano=datetime.now().year,
            cor=2,
            combustivel=3
        )
    
    def test_is_new(self):
        self.assertTrue(self.instancia.veiculo_novo)
        self.instancia.ano = datetime.now().year - 5
        self.assertFalse(self.instancia.veiculo_novo)

    def test_years_use(self):
        self.instancia.ano = datetime.now().year - 10
        self.assertEqual(self.instancia.anos_de_uso(), 10)

class TestesViewListarVeiculos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.url = reverse('listar-veiculos')
        Veiculo(marca=1, modelo="Modelo1", ano=2020, cor=1, combustivel=1).save()
    
    def test_listar_veiculos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('lista_veiculos')), 1)


class TestesViewCadastrarVeiculo(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.url = reverse('cadastrar-veiculo')
        
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioVeiculo)

    def test_post(self):
        data = {
            'marca': 1,
            'modelo': 'ABCDE',
            'ano': datetime.now().year,
            'cor': 2,
            'combustivel': 3
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))

        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().modelo, 'ABCDE')

class TestesViewEditarVeiculo(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.force_login(user=self.user)
        self.instancia = Veiculo.objects.create(
            marca=1,
            modelo="ABCDE",
            ano=datetime.now().year,
            cor=2,
            combustivel=3
        )
        self.url = reverse('editar-veiculo', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Veiculo)
        self.assertIsInstance(response.context.get('form'), FormularioVeiculo)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)
        self.assertEqual(response.context.get('object').modelo, self.instancia.modelo)

    def test_post(self):
        data = {
            'marca': 2,
            'modelo': 'FGHIJ',
            'ano': datetime.now().year - 1,
            'cor': 3,
            'combustivel': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))

        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().modelo, 'FGHIJ')
        self.assertEqual(Veiculo.objects.first().marca, 2)
        self.assertEqual(Veiculo.objects.first().pk, self.instancia.pk)

class TestesViewExcluirVeiculo(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.force_login(user=self.user)
        self.instancia = Veiculo.objects.create(
            marca=1,
            modelo="ABCDE",
            ano=datetime.now().year,
            cor=2,
            combustivel=3
        )
        self.url = reverse('excluir-veiculo', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Veiculo)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))

        self.assertEqual(Veiculo.objects.count(), 0)
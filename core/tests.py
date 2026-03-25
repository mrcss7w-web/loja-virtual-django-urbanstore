from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from produtos.models import Categoria, Produto


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cat = Categoria.objects.create(nome='Teste')
        Produto.objects.create(
            nome='Produto Destaque', descricao='Desc', preco='99.90',
            estoque=10, categoria=self.cat, ativo=True, destaque=True
        )

    def test_home_status_200(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_usa_template_correto(self):
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/home.html')

    def test_home_exibe_destaques(self):
        response = self.client.get(reverse('core:home'))
        self.assertIn('destaques', response.context)

    def test_home_publica_sem_login(self):
        """Home deve ser acessível sem autenticação."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')

    def test_login_get_status_200(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # redirect após login

    def test_login_com_credenciais_invalidas(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser', 'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, 200)  # permanece na página

    def test_logout_redireciona(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from produtos.models import Categoria, Produto


class APIAutenticacaoTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apiuser', password='apipass123')
        self.token = Token.objects.create(user=self.user)

    def test_login_api_retorna_token(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'apiuser',
            'password': 'apipass123'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_api_credenciais_invalidas(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'apiuser',
            'password': 'senhaerrada'
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_perfil_sem_token_retorna_401(self):
        response = self.client.get('/api/auth/perfil/')
        self.assertEqual(response.status_code, 401)

    def test_perfil_com_token_retorna_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/auth/perfil/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'apiuser')


class APIProdutosTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apiuser2', password='pass123')
        self.token = Token.objects.create(user=self.user)
        self.cat = Categoria.objects.create(nome='Categoria API')
        self.produto = Produto.objects.create(
            nome='Produto API', descricao='Para teste', preco='199.90',
            estoque=10, categoria=self.cat, ativo=True
        )

    def test_listar_produtos_publico(self):
        """Listagem pública não exige token."""
        response = self.client.get('/api/produtos/')
        self.assertEqual(response.status_code, 200)

    def test_detalhe_produto_publico(self):
        response = self.client.get(f'/api/produtos/{self.produto.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Produto API')

    def test_criar_produto_sem_token_retorna_401(self):
        response = self.client.post('/api/produtos/', {
            'nome': 'Novo', 'descricao': 'Desc', 'preco': '50.00',
            'estoque': 5, 'categoria': self.cat.pk, 'ativo': True
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_criar_produto_com_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/produtos/', {
            'nome': 'Produto Criado via API',
            'descricao': 'Criado via API REST',
            'preco': '299.90',
            'estoque': 20,
            'categoria': self.cat.pk,
            'ativo': True,
            'destaque': False,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Produto.objects.filter(nome='Produto Criado via API').exists())

    def test_editar_produto_com_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(
            f'/api/produtos/{self.produto.pk}/',
            {'nome': 'Produto Editado via API'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Produto Editado via API')

    def test_excluir_produto_com_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        pk = self.produto.pk
        response = self.client.delete(f'/api/produtos/{pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Produto.objects.filter(pk=pk).exists())

    def test_endpoint_destaques_publico(self):
        response = self.client.get('/api/produtos/destaques/')
        self.assertEqual(response.status_code, 200)

    def test_endpoint_sem_estoque_exige_token(self):
        response = self.client.get('/api/produtos/sem_estoque/')
        self.assertEqual(response.status_code, 401)


class APICategoriasTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apicat', password='pass123')
        self.token = Token.objects.create(user=self.user)
        self.cat = Categoria.objects.create(nome='Categoria Teste')

    def test_listar_categorias_publico(self):
        response = self.client.get('/api/categorias/')
        self.assertEqual(response.status_code, 200)

    def test_criar_categoria_sem_token(self):
        response = self.client.post('/api/categorias/', {'nome': 'Nova'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_criar_categoria_com_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/categorias/', {'nome': 'Nova Cat'}, format='json')
        self.assertEqual(response.status_code, 201)

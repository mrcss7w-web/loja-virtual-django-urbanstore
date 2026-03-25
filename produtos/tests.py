from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Produto


class CategoriaModelTest(TestCase):

    def test_str_categoria(self):
        cat = Categoria.objects.create(nome='Camisetas')
        self.assertEqual(str(cat), 'Camisetas')


class ProdutoModelTest(TestCase):

    def setUp(self):
        self.cat = Categoria.objects.create(nome='Calçados')
        self.produto = Produto.objects.create(
            nome='Tênis Top',
            descricao='Tênis muito bom',
            preco='299.90',
            preco_promocional='249.90',
            estoque=10,
            categoria=self.cat,
            ativo=True,
        )

    def test_str_produto(self):
        self.assertEqual(str(self.produto), 'Tênis Top')

    def test_preco_atual_com_promocao(self):
        from decimal import Decimal
        self.assertEqual(self.produto.preco_atual, Decimal('249.90'))

    def test_preco_atual_sem_promocao(self):
        from decimal import Decimal
        self.produto.preco_promocional = None
        self.produto.save()
        self.assertEqual(self.produto.preco_atual, Decimal('299.90'))

    def test_tem_promocao(self):
        self.assertTrue(self.produto.tem_promocao)

    def test_sem_promocao(self):
        self.produto.preco_promocional = None
        self.produto.save()
        self.assertFalse(self.produto.tem_promocao)

    def test_percentual_desconto(self):
        self.assertGreater(self.produto.percentual_desconto, 0)

    def test_disponivel_com_estoque(self):
        self.assertTrue(self.produto.disponivel)

    def test_indisponivel_sem_estoque(self):
        self.produto.estoque = 0
        self.produto.save()
        self.assertFalse(self.produto.disponivel)


class CatalogoPublicoTest(TestCase):
    """Testa que o catálogo é público e não exige login."""

    def setUp(self):
        self.client = Client()
        self.cat = Categoria.objects.create(nome='Jaquetas')
        Produto.objects.create(
            nome='Jaqueta Bomber', descricao='Top', preco='399.90',
            estoque=5, categoria=self.cat, ativo=True
        )
        Produto.objects.create(
            nome='Produto Inativo', descricao='Inativo', preco='99.90',
            estoque=5, categoria=self.cat, ativo=False
        )

    def test_catalogo_publico_status_200(self):
        response = self.client.get(reverse('produtos:catalogo'))
        self.assertEqual(response.status_code, 200)

    def test_catalogo_exibe_apenas_ativos(self):
        response = self.client.get(reverse('produtos:catalogo'))
        nomes = [p.nome for p in response.context['produtos']]
        self.assertIn('Jaqueta Bomber', nomes)
        self.assertNotIn('Produto Inativo', nomes)

    def test_detalhe_produto_publico(self):
        p = Produto.objects.get(nome='Jaqueta Bomber')
        response = self.client.get(reverse('produtos:detalhe', args=[p.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detalhe_produto_inativo_retorna_404(self):
        p = Produto.objects.get(nome='Produto Inativo')
        response = self.client.get(reverse('produtos:detalhe', args=[p.pk]))
        self.assertEqual(response.status_code, 404)


class CRUDAutenticadoTest(TestCase):
    """Testa que CRUD exige autenticação e funciona corretamente."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('admintest', password='pass123')
        self.cat = Categoria.objects.create(nome='Acessórios')
        self.produto = Produto.objects.create(
            nome='Boné', descricao='Boné top', preco='79.90',
            estoque=20, categoria=self.cat, ativo=True
        )

    def test_dashboard_redireciona_sem_login(self):
        response = self.client.get(reverse('produtos:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_criar_produto_redireciona_sem_login(self):
        response = self.client.get(reverse('produtos:criar'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_acessivel_com_login(self):
        self.client.login(username='admintest', password='pass123')
        response = self.client.get(reverse('produtos:admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_criar_produto_post_valido(self):
        self.client.login(username='admintest', password='pass123')
        response = self.client.post(reverse('produtos:criar'), {
            'nome': 'Novo Produto',
            'descricao': 'Descrição do produto',
            'preco': '149.90',
            'preco_promocional': '',
            'estoque': 15,
            'categoria': self.cat.pk,
            'imagem_url': '',
            'ativo': True,
            'destaque': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Produto.objects.filter(nome='Novo Produto').exists())

    def test_editar_produto(self):
        self.client.login(username='admintest', password='pass123')
        response = self.client.post(
            reverse('produtos:editar', args=[self.produto.pk]),
            {
                'nome': 'Boné Editado',
                'descricao': 'Nova descrição',
                'preco': '89.90',
                'preco_promocional': '',
                'estoque': 25,
                'categoria': self.cat.pk,
                'imagem_url': '',
                'ativo': True,
                'destaque': False,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Boné Editado')

    def test_excluir_produto(self):
        self.client.login(username='admintest', password='pass123')
        pk = self.produto.pk
        response = self.client.post(reverse('produtos:excluir', args=[pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Produto.objects.filter(pk=pk).exists())

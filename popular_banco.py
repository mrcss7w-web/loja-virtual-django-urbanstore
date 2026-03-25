"""
Script para popular o banco com dados de exemplo.
Execute: python popular_banco.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loja_virtual.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from produtos.models import Categoria, Produto

print("🛍 Populando banco de dados da UrbanStore...\n")

# Superusuário
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@urbanstore.com', 'admin123')
    admin.first_name = 'Admin'
    admin.save()
    Token.objects.get_or_create(user=admin)
    print("  ✔ Superusuário criado: admin / admin123")
else:
    admin = User.objects.get(username='admin')
    Token.objects.get_or_create(user=admin)
    print("  ✔ Superusuário já existe")

# Categorias
cats_data = [
    ('Camisetas', 'Camisetas masculinas e femininas de alta qualidade'),
    ('Calçados', 'Tênis, sapatos e sandálias das melhores marcas'),
    ('Acessórios', 'Bonés, cintos, óculos e muito mais'),
    ('Jaquetas', 'Jaquetas e casacos para todos os estilos'),
    ('Calças', 'Jeans, moletom e calças esportivas'),
]
cats = {}
for nome, desc in cats_data:
    cat, c = Categoria.objects.get_or_create(nome=nome, defaults={'descricao': desc})
    cats[nome] = cat
    if c: print(f"  ✔ Categoria: {nome}")

# Produtos
produtos_data = [
    {
        'nome': 'Camiseta Street Premium',
        'descricao': 'Camiseta de algodão premium com corte oversize. Perfeita para o dia a dia urbano.',
        'preco': '89.90', 'preco_promocional': '69.90', 'estoque': 50,
        'categoria': 'Camisetas', 'ativo': True, 'destaque': True,
        'imagem_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600'
    },
    {
        'nome': 'Camiseta Basic Preta',
        'descricao': 'Camiseta básica preta, essencial para qualquer guarda-roupa.',
        'preco': '59.90', 'preco_promocional': None, 'estoque': 120,
        'categoria': 'Camisetas', 'ativo': True, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=600'
    },
    {
        'nome': 'Tênis Urban Runner',
        'descricao': 'Tênis esportivo com solado de alta tecnologia. Ideal para corrida e uso casual.',
        'preco': '349.90', 'preco_promocional': '299.90', 'estoque': 30,
        'categoria': 'Calçados', 'ativo': True, 'destaque': True,
        'imagem_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600'
    },
    {
        'nome': 'Tênis Classic White',
        'descricao': 'Tênis branco clássico. Combina com qualquer look.',
        'preco': '289.90', 'preco_promocional': None, 'estoque': 0,
        'categoria': 'Calçados', 'ativo': True, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=600'
    },
    {
        'nome': 'Boné Snapback Preto',
        'descricao': 'Boné snapback com aba reta. Bordado lateral exclusivo.',
        'preco': '79.90', 'preco_promocional': '59.90', 'estoque': 85,
        'categoria': 'Acessórios', 'ativo': True, 'destaque': True,
        'imagem_url': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600'
    },
    {
        'nome': 'Jaqueta Bomber Urban',
        'descricao': 'Jaqueta bomber com forro interno. Resistente ao vento.',
        'preco': '459.90', 'preco_promocional': '389.90', 'estoque': 20,
        'categoria': 'Jaquetas', 'ativo': True, 'destaque': True,
        'imagem_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600'
    },
    {
        'nome': 'Calça Jeans Slim',
        'descricao': 'Calça jeans slim fit, corte moderno e confortável.',
        'preco': '199.90', 'preco_promocional': None, 'estoque': 60,
        'categoria': 'Calças', 'ativo': True, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1542574271-7f3b92e6c821?w=600'
    },
    {
        'nome': 'Calça Moletom Street',
        'descricao': 'Moletom de algodão com elástico na cintura. Máximo conforto.',
        'preco': '149.90', 'preco_promocional': '119.90', 'estoque': 40,
        'categoria': 'Calças', 'ativo': True, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1565084888279-aca607ecce0c?w=600'
    },
    {
        'nome': 'Jaqueta Corta-Vento',
        'descricao': 'Leve, impermeável e dobrável. Perfeita para aventuras.',
        'preco': '319.90', 'preco_promocional': None, 'estoque': 15,
        'categoria': 'Jaquetas', 'ativo': True, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600'
    },
    {
        'nome': 'Camiseta Tie-Dye',
        'descricao': 'Camiseta tie-dye artesanal. Peça única, produção limitada.',
        'preco': '99.90', 'preco_promocional': None, 'estoque': 0,
        'categoria': 'Camisetas', 'ativo': False, 'destaque': False,
        'imagem_url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600'
    },
]

for dados in produtos_data:
    p, criado = Produto.objects.get_or_create(
        nome=dados['nome'],
        defaults={
            'descricao': dados['descricao'],
            'preco': dados['preco'],
            'preco_promocional': dados.get('preco_promocional'),
            'estoque': dados['estoque'],
            'categoria': cats[dados['categoria']],
            'imagem_url': dados['imagem_url'],
            'ativo': dados['ativo'],
            'destaque': dados['destaque'],
            'criado_por': admin,
        }
    )
    if criado:
        print(f"  ✔ Produto: {dados['nome']}")

token = Token.objects.get(user=admin)
print(f"\n{'='*55}")
print(f"✅ Banco populado com sucesso!")
print(f"   {Categoria.objects.count()} categorias | {Produto.objects.count()} produtos")
print(f"\n🔑 Acesso Admin:")
print(f"   Usuário: admin  |  Senha: admin123")
print(f"\n⚡ Token da API:")
print(f"   {token.key}")
print(f"\n📌 Como usar a API:")
print(f"   Authorization: Token {token.key}")
print(f"\n🌐 Acesse: http://127.0.0.1:8000")
print(f"{'='*55}")

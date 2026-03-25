from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm


# ─── VIEWS PÚBLICAS ───────────────────────────────────────────────────────────

def catalogo(request):
    produtos = Produto.objects.filter(ativo=True).select_related('categoria')
    busca = request.GET.get('busca', '')
    ordenacao = request.GET.get('ordem', '-criado_em')

    # Filtro categoria com validação
    categoria_id = request.GET.get('categoria', '')
    try:
        if categoria_id:
            produtos = produtos.filter(categoria_id=int(categoria_id))
    except (ValueError, TypeError):
        categoria_id = ''

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | Q(descricao__icontains=busca)
        )

    ordens_validas = ['-criado_em', 'preco', '-preco', 'nome']
    if ordenacao in ordens_validas:
        produtos = produtos.order_by(ordenacao)

    categorias = Categoria.objects.all()

    return render(request, 'produtos/catalogo.html', {
        'titulo': 'Catálogo de Produtos',
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
        'categoria_selecionada': categoria_id,
        'ordenacao': ordenacao,
        'total': produtos.count(),
    })


def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    relacionados = Produto.objects.filter(
        categoria=produto.categoria, ativo=True
    ).exclude(pk=pk)[:4]

    return render(request, 'produtos/detalhe.html', {
        'titulo': produto.nome,
        'produto': produto,
        'relacionados': relacionados,
    })


# ─── VIEWS ADMINISTRATIVAS ────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    total_produtos = Produto.objects.count()
    produtos_ativos = Produto.objects.filter(ativo=True).count()
    produtos_destaque = Produto.objects.filter(destaque=True).count()
    sem_estoque = Produto.objects.filter(estoque=0, ativo=True).count()
    total_categorias = Categoria.objects.count()
    ultimos_produtos = Produto.objects.order_by('-criado_em')[:5]

    return render(request, 'produtos/admin_dashboard.html', {
        'titulo': 'Dashboard — Área Administrativa',
        'total_produtos': total_produtos,
        'produtos_ativos': produtos_ativos,
        'produtos_destaque': produtos_destaque,
        'sem_estoque': sem_estoque,
        'total_categorias': total_categorias,
        'ultimos_produtos': ultimos_produtos,
    })


@login_required
def admin_lista_produtos(request):
    produtos = Produto.objects.all().select_related('categoria', 'criado_por')
    busca = request.GET.get('busca', '')
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | Q(categoria__nome__icontains=busca)
        )
    return render(request, 'produtos/admin_lista.html', {
        'titulo': 'Gerenciar Produtos',
        'produtos': produtos,
        'busca': busca,
    })


@login_required
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.criado_por = request.user
            produto.save()
            messages.success(request, f'Produto "{produto.nome}" cadastrado com sucesso!')
            return redirect('produtos:admin_lista')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm()

    return render(request, 'produtos/produto_form.html', {
        'titulo': 'Cadastrar Produto', 'form': form, 'acao': 'Cadastrar',
    })


@login_required
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('produtos:admin_lista')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produtos/produto_form.html', {
        'titulo': f'Editar: {produto.nome}', 'form': form,
        'produto': produto, 'acao': 'Salvar Alterações',
    })


@login_required
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'Produto "{nome}" excluído com sucesso!')
        return redirect('produtos:admin_lista')
    return render(request, 'produtos/produto_confirmar_exclusao.html', {
        'titulo': f'Excluir: {produto.nome}', 'produto': produto,
    })


# ─── CATEGORIAS ───────────────────────────────────────────────────────────────

@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/categoria_lista.html', {
        'titulo': 'Gerenciar Categorias', 'categorias': categorias,
    })


@login_required
def categoria_criar(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" criada!')
            return redirect('produtos:categoria_lista')
    else:
        form = CategoriaForm()
    return render(request, 'produtos/categoria_form.html', {
        'titulo': 'Nova Categoria', 'form': form, 'acao': 'Criar',
    })


@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoria "{categoria.nome}" atualizada!')
            return redirect('produtos:categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'produtos/categoria_form.html', {
        'titulo': f'Editar: {categoria.nome}', 'form': form, 'acao': 'Salvar',
    })


@login_required
def categoria_excluir(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nome = categoria.nome
        categoria.delete()
        messages.success(request, f'Categoria "{nome}" excluída!')
        return redirect('produtos:categoria_lista')
    return render(request, 'produtos/categoria_confirmar_exclusao.html', {
        'titulo': f'Excluir: {categoria.nome}', 'categoria': categoria,
    })

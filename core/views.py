from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from produtos.models import Produto, Categoria


def home(request):
    """Página inicial pública com produtos em destaque."""
    destaques = Produto.objects.filter(ativo=True, destaque=True).select_related('categoria')[:8]
    lancamentos = Produto.objects.filter(ativo=True).order_by('-criado_em')[:8]
    categorias = Categoria.objects.all()
    total_produtos = Produto.objects.filter(ativo=True).count()

    return render(request, 'core/home.html', {
        'titulo': 'UrbanStore — Loja Virtual',
        'destaques': destaques,
        'lancamentos': lancamentos,
        'categorias': categorias,
        'total_produtos': total_produtos,
    })


def login_view(request):
    """Página de login."""
    if request.user.is_authenticated:
        return redirect('produtos:admin_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'produtos:admin_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {
        'titulo': 'Login — UrbanStore',
        'form': form,
    })


def logout_view(request):
    """Logout."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Você saiu com segurança.')
    return redirect('core:home')

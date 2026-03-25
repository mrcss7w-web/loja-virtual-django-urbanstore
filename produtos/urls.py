from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Público
    path('', views.catalogo, name='catalogo'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe'),

    # Área administrativa (requer login)
    path('admin-loja/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-loja/lista/', views.admin_lista_produtos, name='admin_lista'),
    path('admin-loja/novo/', views.produto_criar, name='criar'),
    path('admin-loja/editar/<int:pk>/', views.produto_editar, name='editar'),
    path('admin-loja/excluir/<int:pk>/', views.produto_excluir, name='excluir'),

    # Categorias
    path('admin-loja/categorias/', views.categoria_lista, name='categoria_lista'),
    path('admin-loja/categorias/nova/', views.categoria_criar, name='categoria_criar'),
    path('admin-loja/categorias/editar/<int:pk>/', views.categoria_editar, name='categoria_editar'),
    path('admin-loja/categorias/excluir/<int:pk>/', views.categoria_excluir, name='categoria_excluir'),
]

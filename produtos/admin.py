from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'estoque', 'ativo', 'destaque', 'criado_em']
    list_filter = ['ativo', 'destaque', 'categoria']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo', 'destaque', 'estoque']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_por', 'criado_em', 'atualizado_em']

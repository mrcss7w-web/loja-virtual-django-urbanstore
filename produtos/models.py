from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço (R$)')
    preco_promocional = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Preço Promocional (R$)'
    )
    estoque = models.PositiveIntegerField(default=0, verbose_name='Estoque')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='produtos',
        verbose_name='Categoria'
    )
    imagem_url = models.URLField(
        blank=True,
        verbose_name='URL da Imagem',
        help_text='Cole a URL de uma imagem do produto'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo (visível na loja)')
    destaque = models.BooleanField(default=False, verbose_name='Produto em Destaque')
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produtos_criados',
        verbose_name='Criado por'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome

    @property
    def preco_atual(self):
        """Retorna o preço promocional se existir, senão o preço normal."""
        if self.preco_promocional:
            return self.preco_promocional
        return self.preco

    @property
    def tem_promocao(self):
        return self.preco_promocional is not None and self.preco_promocional < self.preco

    @property
    def percentual_desconto(self):
        if self.tem_promocao:
            desconto = ((self.preco - self.preco_promocional) / self.preco) * 100
            return round(desconto)
        return 0

    @property
    def disponivel(self):
        return self.ativo and self.estoque > 0

from django import forms
from .models import Produto, Categoria


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'descricao', 'preco', 'preco_promocional',
            'estoque', 'categoria', 'imagem_url', 'ativo', 'destaque'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do produto'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Descrição detalhada do produto'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'preco_promocional': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': 'Deixe vazio se não houver promoção'
            }),
            'estoque': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-input'
            }),
            'imagem_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://exemplo.com/imagem.jpg'
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'destaque': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'nome': 'Nome do Produto',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'preco_promocional': 'Preço Promocional (R$)',
            'estoque': 'Quantidade em Estoque',
            'categoria': 'Categoria',
            'imagem_url': 'URL da Imagem',
            'ativo': 'Produto ativo (visível na loja)',
            'destaque': 'Exibir em destaque na home',
        }

    def clean_preco_promocional(self):
        preco = self.cleaned_data.get('preco')
        preco_promo = self.cleaned_data.get('preco_promocional')
        if preco_promo and preco and preco_promo >= preco:
            raise forms.ValidationError(
                'O preço promocional deve ser menor que o preço normal.'
            )
        return preco_promo


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome da categoria'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Descrição da categoria (opcional)'
            }),
        }

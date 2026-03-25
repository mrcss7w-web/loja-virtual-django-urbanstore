from rest_framework import serializers
from produtos.models import Produto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    total_produtos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'total_produtos', 'criado_em']
        read_only_fields = ['id', 'criado_em']

    def get_total_produtos(self, obj):
        return obj.produtos.filter(ativo=True).count()


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    preco_atual = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tem_promocao = serializers.BooleanField(read_only=True)
    percentual_desconto = serializers.IntegerField(read_only=True)
    disponivel = serializers.BooleanField(read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'preco', 'preco_promocional',
            'preco_atual', 'tem_promocao', 'percentual_desconto',
            'estoque', 'disponivel', 'categoria', 'categoria_nome',
            'imagem_url', 'ativo', 'destaque', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_preco_promocional(self, value):
        preco = self.initial_data.get('preco') or (
            self.instance.preco if self.instance else None
        )
        if value and preco and float(value) >= float(preco):
            raise serializers.ValidationError(
                'O preço promocional deve ser menor que o preço normal.'
            )
        return value


class ProdutoListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listagem."""
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    preco_atual = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tem_promocao = serializers.BooleanField(read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'preco', 'preco_atual', 'tem_promocao',
            'estoque', 'categoria_nome', 'imagem_url', 'ativo', 'destaque'
        ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço (R$)')),
                ('preco_promocional', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço Promocional (R$)')),
                ('estoque', models.PositiveIntegerField(default=0, verbose_name='Estoque')),
                ('imagem_url', models.URLField(blank=True, help_text='Cole a URL de uma imagem do produto', verbose_name='URL da Imagem')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo (visível na loja)')),
                ('destaque', models.BooleanField(default=False, verbose_name='Produto em Destaque')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produtos', to='produtos.categoria', verbose_name='Categoria')),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produtos_criados', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['-criado_em'],
            },
        ),
    ]

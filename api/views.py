from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from produtos.models import Produto, Categoria
from .serializers import ProdutoSerializer, ProdutoListSerializer, CategoriaSerializer


# ─── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'erro': 'Informe username e password.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'mensagem': 'Login realizado com sucesso. Use: Authorization: Token <token>',
        })
    return Response({'erro': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'mensagem': 'Logout realizado. Token invalidado.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_perfil(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'nome': user.get_full_name() or user.username,
        'is_staff': user.is_staff,
    })


# ─── CATEGORIAS ───────────────────────────────────────────────────────────────

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('nome')
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'criado_em']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


# ─── PRODUTOS ─────────────────────────────────────────────────────────────────

class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao', 'categoria__nome']
    ordering_fields = ['nome', 'preco', 'estoque', 'criado_em']
    ordering = ['-criado_em']

    def get_queryset(self):
        queryset = Produto.objects.select_related('categoria', 'criado_por')

        categoria = self.request.query_params.get('categoria')
        destaque = self.request.query_params.get('destaque')
        preco_min = self.request.query_params.get('preco_min')
        preco_max = self.request.query_params.get('preco_max')

        # Filtro ativo — usuário não autenticado só vê ativos
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(ativo=True)
        else:
            ativo = self.request.query_params.get('ativo')
            if ativo is not None:
                queryset = queryset.filter(ativo=ativo.lower() == 'true')

        try:
            if categoria:
                queryset = queryset.filter(categoria_id=int(categoria))
        except (ValueError, TypeError):
            pass

        if destaque is not None:
            queryset = queryset.filter(destaque=destaque.lower() == 'true')

        try:
            if preco_min:
                queryset = queryset.filter(preco__gte=float(preco_min))
            if preco_max:
                queryset = queryset.filter(preco__lte=float(preco_max))
        except (ValueError, TypeError):
            pass

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ProdutoListSerializer
        return ProdutoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destaques']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def destaques(self, request):
        produtos = Produto.objects.filter(ativo=True, destaque=True).select_related('categoria')
        page = self.paginate_queryset(produtos)
        if page is not None:
            serializer = ProdutoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProdutoListSerializer(produtos, many=True)
        return Response({'count': produtos.count(), 'results': serializer.data})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def sem_estoque(self, request):
        produtos = self.get_queryset().filter(estoque=0)
        page = self.paginate_queryset(produtos)
        if page is not None:
            serializer = ProdutoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProdutoListSerializer(produtos, many=True)
        return Response({'count': produtos.count(), 'results': serializer.data})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def todos(self, request):
        produtos = Produto.objects.all().select_related('categoria')
        page = self.paginate_queryset(produtos)
        if page is not None:
            serializer = ProdutoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProdutoListSerializer(produtos, many=True)
        return Response({'count': produtos.count(), 'results': serializer.data})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_ativo(self, request, pk=None):
        produto = self.get_object()
        produto.ativo = not produto.ativo
        produto.save()
        estado = 'ativado' if produto.ativo else 'desativado'
        return Response({'mensagem': f'Produto "{produto.nome}" {estado}.', 'ativo': produto.ativo})

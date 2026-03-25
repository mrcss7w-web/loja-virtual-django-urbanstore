from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'produtos', views.ProdutoViewSet, basename='produto')
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    # Autenticação
    path('auth/login/', views.api_login, name='api_login'),
    path('auth/logout/', views.api_logout, name='api_logout'),
    path('auth/perfil/', views.api_perfil, name='api_perfil'),

    # ViewSets (CRUD automático via router)
    path('', include(router.urls)),
]

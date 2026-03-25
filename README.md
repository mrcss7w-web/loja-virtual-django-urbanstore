# 🛍️ UrbanStore — Loja Virtual

> **Desafio Final do Módulo de Django**
> Curso de Back-End com Python · IFMG Bambuí

---

## 📋 Sobre o Projeto

O UrbanStore** é uma loja virtual completa, construída com Django e Django REST Framework. Oferece:

---

## 🚀 Como Executar no VS Code

### Pré-requisitos
- [Python 3.10+](https://python.org/downloads) — marque "Add to PATH"
- [VS Code](https://code.visualstudio.com)
- Extensão **Python** (Microsoft) no VS Code

---

### ▶️ Opção 1 — Setup Automático (recomendado)

**Windows:**
```
Duplo clique em setup.bat
```

**Linux / Mac:**
```bash
chmod +x setup.sh && ./setup.sh
```

Depois de concluído:
```bash
# Windows
.venv\Scripts\activate
python manage.py runserver

# Linux/Mac
source .venv/bin/activate
python manage.py runserver
```

---

### 🔧 Opção 2 — Passo a Passo Manual no VS Code

#### 1. Abrir o projeto
```
File → Open Folder → selecione a pasta loja_virtual
```

#### 2. Abrir o terminal integrado
```
Ctrl + ` (acento grave)
```

#### 3. Criar o ambiente virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

> **VS Code vai perguntar:** "We noticed a new virtual environment..." → clique **Yes** para selecionar automaticamente.

#### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 5. Criar o banco de dados
```bash
python manage.py migrate
```

#### 6. Popular com dados de exemplo
```bash
python popular_banco.py
```
> Cria 5 categorias, 10 produtos, superusuário **admin / admin123** e o token da API.

#### 7. Rodar o servidor
```bash
python manage.py runserver
```

#### 8. Abrir no navegador
```
http://127.0.0.1:8000
```

---

### ⚡ Debug no VS Code (F5)

O projeto já tem `.vscode/launch.json` configurado:

1. Pressione **F5** ou vá em **Run → Start Debugging**
2. Selecione **"▶ Rodar Django"**
3. O servidor inicia com breakpoints ativos

Para rodar os testes com debug:
- Selecione **"🧪 Rodar Testes"** e pressione F5

---

### 🧪 Rodar os Testes

```bash
python manage.py test --verbosity=2
```

Ou via VS Code: **F5 → "🧪 Rodar Testes"**

Cobertura dos testes:
- Models (Categoria, Produto, propriedades calculadas)
- Views públicas (catálogo, 404 para inativos)
- CRUD administrativo (redirect sem login, funcionamento com login)
- API REST (autenticação, CRUD, permissões, filtros)

---

## 🌐 URLs do Sistema

| URL | Descrição | Acesso |
|---|---|---|
| `http://127.0.0.1:8000/` | Home pública com destaques | Público |
| `http://127.0.0.1:8000/produtos/` | Catálogo com filtros | Público |
| `http://127.0.0.1:8000/produtos/1/` | Detalhe de produto | Público |
| `http://127.0.0.1:8000/login/` | Login | Público |
| `http://127.0.0.1:8000/produtos/admin-loja/` | Dashboard admin | 🔒 Login |
| `http://127.0.0.1:8000/api/` | API REST (Browsable) | Misto |
| `http://127.0.0.1:8000/django-admin/` | Admin Django | 🔒 Login |

---

## ⚡ API REST

### Autenticação
```bash
POST /api/auth/login/
Content-Type: application/json

{ "username": "admin", "password": "admin123" }
```

**Resposta:**
```json
{ "token": "abc123...", "username": "admin" }
```

**Usar o token:**
```
Authorization: Token abc123...
```

### Endpoints

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| GET | `/api/produtos/` | Público | Lista ativos (paginado) |
| GET | `/api/produtos/{id}/` | Público | Detalhe |
| POST | `/api/produtos/` | 🔒 Token | Criar |
| PUT/PATCH | `/api/produtos/{id}/` | 🔒 Token | Editar |
| DELETE | `/api/produtos/{id}/` | 🔒 Token | Excluir |
| GET | `/api/produtos/destaques/` | Público | Em destaque |
| GET | `/api/produtos/sem_estoque/` | 🔒 Token | Sem estoque |
| POST | `/api/produtos/{id}/toggle_ativo/` | 🔒 Token | Ativar/desativar |
| GET | `/api/categorias/` | Público | Lista categorias |
| POST | `/api/auth/login/` | Público | Obter token |
| POST | `/api/auth/logout/` | 🔒 Token | Invalidar token |
| GET | `/api/auth/perfil/` | 🔒 Token | Dados do usuário |

### Filtros e Busca
```bash
GET /api/produtos/?search=camiseta
GET /api/produtos/?categoria=1
GET /api/produtos/?preco_min=50&preco_max=200
GET /api/produtos/?destaque=true
GET /api/produtos/?ordering=preco
GET /api/produtos/?page=2
```

---

## 🏗️ Estrutura do Projeto

```
loja_virtual/
├── .vscode/
│   ├── settings.json       # Configurações VSCode + Django HTML
│   ├── launch.json         # Debug F5 (runserver + testes)
│   └── extensions.json     # Extensões recomendadas
├── manage.py
├── requirements.txt
├── popular_banco.py
├── setup.bat               # Setup automático Windows
├── setup.sh                # Setup automático Linux/Mac
│
├── loja_virtual/           # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   # App base: autenticação e home
│   ├── views.py
│   ├── urls.py
│   ├── static/core/
│   │   ├── css/style.css   # Design Glassmorphism completo
│   │   └── js/script.js    # Dark mode, nav mobile, alerts
│   └── templates/core/
│       ├── base.html       # Template base com toggle de tema
│       ├── home.html
│       └── login.html
│
├── produtos/               # App principal: CRUD
│   ├── models.py
│   ├── views.py            # Catálogo (público) + CRUD (privado)
│   ├── forms.py
│   ├── urls.py
│   └── templates/produtos/
│       ├── catalogo.html
│       ├── detalhe.html
│       ├── admin_dashboard.html
│       ├── admin_lista.html
│       ├── produto_form.html
│       └── ...
│
└── api/                    # App API REST
    ├── views.py            # ViewSets + auth + filtros seguros
    ├── serializers.py
    └── urls.py
```

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **Django 4.2+**
- **Django REST Framework 3.14+**
- **django-filter 23+**
- **SQLite** (desenvolvimento)
- **CSS Glassmorphism** customizado (sem frameworks externos)
- **Inter + Bebas Neue** (Google Fonts)

---

## 🔐 Segurança Implementada

- `@login_required` em todas as views administrativas
- Validação de tipo nos filtros (ex: `categoria_id` int)
- `api_logout` com try/except (token inexistente não quebra)
- `get_object_or_404` em todas as views de detalhe
- Filtragem de produtos inativos para usuários não autenticados
- `preco_promocional` validado menor que `preco` (form + serializer)

---

*UrbanStore — Desafio Final Django · IFMG Bambuí*

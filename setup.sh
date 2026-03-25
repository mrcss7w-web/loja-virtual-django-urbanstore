#!/bin/bash
set -e

echo "========================================"
echo " UrbanStore — Setup Automatico (Linux/Mac)"
echo "========================================"

# 1. Cria venv
python3 -m venv .venv || { echo "ERRO: python3 nao encontrado."; exit 1; }

# 2. Ativa e instala
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

# 3. Migrations
python manage.py migrate

# 4. Popula banco
python popular_banco.py

echo ""
echo "========================================"
echo " Setup concluido!"
echo " Rode: source .venv/bin/activate && python manage.py runserver"
echo " Acesse: http://127.0.0.1:8000"
echo " Login: admin / admin123"
echo "========================================"

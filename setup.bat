@echo off
echo ========================================
echo  UrbanStore — Setup Automatico (Windows)
echo ========================================

:: 1. Cria o ambiente virtual
python -m venv .venv
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Instale em https://python.org
    pause
    exit /b 1
)

:: 2. Ativa e instala dependencias
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO ao instalar dependencias.
    pause
    exit /b 1
)

:: 3. Migrations e banco
python manage.py migrate
if errorlevel 1 (
    echo ERRO nas migrations.
    pause
    exit /b 1
)

:: 4. Popula banco com dados de exemplo
python popular_banco.py

echo.
echo ========================================
echo  Setup concluido!
echo  Rode agora: python manage.py runserver
echo  Acesse:     http://127.0.0.1:8000
echo  Login:      admin / admin123
echo ========================================
pause

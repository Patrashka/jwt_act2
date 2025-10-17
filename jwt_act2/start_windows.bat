@echo off
echo Configurando sistema de autenticacion JWT...
echo.

echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo Configurando base de datos...
python setup_windows.py
if %errorlevel% neq 0 (
    echo Error configurando base de datos
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion...
echo.
echo ========================================
echo   SISTEMA DE AUTENTICACION JWT
echo ========================================
echo.
echo Frontend: http://localhost:5000
echo API: http://localhost:5000/api
echo Usuario de ejemplo: admin / admin123
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.

python app.py

pause

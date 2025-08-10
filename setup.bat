@echo off
echo ====================================
echo   Setup del Proyecto Python
echo ====================================

REM Verificar si existe el entorno virtual
if exist ".venv" (
    echo Entorno virtual encontrado.
) else (
    echo Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo Error al crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Entorno virtual creado exitosamente.
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Verificar si existe requirements.txt
if exist "requirements.txt" (
    echo Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
) else (
    echo No se encontró requirements.txt, instalando dependencias básicas...
    pip install sympy matplotlib numpy
)

echo.
echo ====================================
echo   Setup completado exitosamente
echo ====================================
echo.
echo Para activar manualmente el entorno virtual, ejecuta:
echo .venv\Scripts\activate
echo.
echo Para ejecutar tu script:
echo python STF.py
echo.
pause
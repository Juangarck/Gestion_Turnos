@echo off
:: Verifica si el proceso php.exe ya está corriendo
tasklist /FI "IMAGENAME eq php.exe" | find /I "php.exe" >nul
if not errorlevel 1 (
    echo El servidor PHP ya está corriendo.
    exit /b
)

:: Si no está corriendo, ejecuta el servidor PHP
start "" "C:\xampp\php\php.exe" "C:\xampp\php\server.php"

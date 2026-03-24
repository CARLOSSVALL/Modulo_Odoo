@echo off
title Lanzar Odoo a Internet (Ngrok)
color 0A

echo =======================================================================
echo =             ACTIVANDO RED PUBLICA PARA ODOO (NGROK)                 =
echo =======================================================================
echo.
echo Se esta generando un túnel hacia tu servidor de Odoo (Puerto 8069).
echo.
echo [INSTRUCCIONES:]
echo Cuando termine de cargar, copia el enlace en la linea que dice "Forwarding".
echo.
echo PARA DESACTIVAR LA RED: Simplemente CIERRA esta ventana negra, o pulsa "Ctrl + C"
echo =======================================================================
echo.

ngrok http 8069

echo.
pause

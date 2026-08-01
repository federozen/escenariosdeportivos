@echo off
setlocal
python -m pip install -r requirements.txt
if errorlevel 1 goto error
python -m streamlit run calculadora_futbol_argentino.py
goto end
:error
echo.
echo No se pudo instalar o iniciar la aplicacion. Revisa que Python este instalado y en PATH.
pause
:end
endlocal

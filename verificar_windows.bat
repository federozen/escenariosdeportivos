@echo off
setlocal
python -m py_compile calculadora_futbol_argentino.py lpf_models.py lpf_data_quality.py lpf_scenarios.py lpf_exact.py
if errorlevel 1 goto error
python -m pytest -q
if errorlevel 1 goto error
echo.
echo Verificacion completada correctamente.
pause
goto end
:error
echo.
echo La verificacion encontro un error.
pause
:end
endlocal

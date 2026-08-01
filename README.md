# Calculadora del Fútbol Argentino · LPF 2026 · versión 3.2

Aplicación editorial en Python y Streamlit para analizar playoffs por zonas, Tabla Anual, Libertadores, Sudamericana, descenso, promedios y escenarios de una fecha.

La versión 3 prioriza tres objetivos:

1. **Base coherente:** Zonas, Tabla Anual, promedios, fixture y resultados se reconcilian antes de habilitar una cuenta.
2. **Explicación honesta:** distingue hechos exactos, garantías matemáticas, cotas conservadoras y estimaciones.
3. **Uso guiado:** ya no es necesario recordar preguntas del chat; el Explorador permite elegir equipo, objetivo y tarea.

## Instalación

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run calculadora_futbol_argentino.py
```

## Espacios de trabajo

- **Panel por equipo:** acceso principal. Elegí equipo, objetivo y pregunta.
- **Escenarios:** herramientas adaptadas de la calculadora del Mundial: gana/empata/pierde, qué pasa si, puesto puntual, mejor/peor caso, distribución y clasificados/eliminados.
- **Mesa de redacción:** informes de previa y post fecha listos para trabajar.
- **Visualizaciones:** vistas por equipo, zona, próxima fecha, otra cancha y Radar final.
- **Chat libre:** consultas abiertas y seguimientos contextuales.
- **Datos y auditoría:** semáforo de calidad, inconsistencias, partidos inferidos y respaldo.

## Flujo recomendado

1. Cargar la foto offline, actualizar desde el proveedor disponible o pegar los datos.
2. Abrir **Datos y auditoría**.
3. Corregir cualquier bloqueo de Zonas, Tabla Anual o Promedios.
4. Trabajar desde el **Panel por equipo**.
5. Abrir **Escenarios** para explorar combinaciones concretas sin recordar comandos.
6. Abrir **Visualizaciones** o **Mesa de redacción** para profundizar y publicar.

## Cuatro referencias distintas

La aplicación evita llamar “piso” a números diferentes:

- **Corte actual:** puntos que tiene hoy el último clasificado.
- **Mínimo todavía posible:** menor puntaje con el que existe una combinación favorable.
- **Garantía matemática:** puntaje con el que entra sin depender de otros resultados ni desempates.
- **Corte estimado:** rango probable de la simulación; nunca se presenta como certeza.

Cuando quedan más de seis partidos, el informe puede usar una **garantía conservadora**. Esa cota es segura, pero podría pedir algún punto de más. Con seis partidos o menos, el Radar habilita un optimizador exacto para construir la escalera de puntajes.

## Datos y fuente de verdad

La prioridad de la versión 3 es:

1. Resultados explícitos para identificar partidos jugados.
2. Foto fija del Apertura más las zonas vigentes para reconstruir la Tabla Anual.
3. Tabla Anual directa solamente si pasa los controles.
4. Inferencia por PJ únicamente como respaldo, siempre rotulada.

Los partidos tienen identidad propia. Un encuentro postergado no se considera jugado solo porque el equipo haya disputado una fecha posterior.

## Exacto, garantía y estimación

- **Exacto:** puntos, PJ, techo, rango por resultados, escenarios factibles y escalera calculada por optimización.
- **Garantía conservadora:** línea segura usada cuando el cálculo exacto completo no se activa.
- **Estimado:** Monte Carlo, dificultad, corte probable e impacto de otras canchas.

El modelo de lenguaje opcional interpreta consultas y redacta. Los números salen siempre de Python.

## Arquitectura

- `calculadora_futbol_argentino.py`: aplicación y compatibilidad con la versión anterior.
- `lpf_models.py`: objetos de dominio, auditoría y resultados estructurados.
- `lpf_data_quality.py`: normalización y reconciliación de Zonas, Anual, Promedios, fixture y resultados.
- `lpf_scenarios.py`: optimización exacta para escalera, rangos y ventanas con postergados.
- `lpf_exact.py`: núcleo determinístico original y cotas seguras.
- `tests/`: pruebas unitarias, fuerza bruta e invariantes.

Más detalle en [ARCHITECTURE.md](ARCHITECTURE.md).

## Verificación

```bash
python -m py_compile calculadora_futbol_argentino.py lpf_models.py lpf_data_quality.py lpf_scenarios.py lpf_exact.py
python -m pytest -q
```

## Documentación

- `AUDITORIA.md`: reglas, alcance de exactitud y controles.
- `ARCHITECTURE.md`: flujo técnico y módulos.
- `GUIA_REDACCION.md`: uso diario y criterio de publicación.
- `GUIA_DATOS.md`: actualización, reconciliación y resolución de conflictos.
- `CHANGELOG.md`: cambios de esta versión.

# Auditoría de reglas, datos y cálculos · versión 3

Fecha de implementación: 1 de agosto de 2026.

## Regla editorial central

La aplicación diferencia:

- hecho exacto;
- garantía matemática exacta;
- garantía conservadora;
- clasificación condicionada;
- estimación.

Ninguna cota conservadora se presenta como mínimo exacto.

## Controles de base

### Zonas

- 15 equipos por zona y 30 únicos.
- PJ y puntos posibles.
- DG coherente con GF-GA cuando están disponibles.
- ausencia de duplicados.

### Fixture y resultados

- cada partido tiene identidad;
- resultados explícitos prioritarios;
- detección de marcadores contradictorios;
- postergados preservados aunque se haya jugado una jornada posterior;
- inferencia por PJ marcada como advertencia.

### Tabla Anual

- mismos clubes que las zonas;
- diferencia de PJ compatible con 16 partidos del Apertura;
- Apertura reconstruible con valores posibles;
- Anual autoritativa = Apertura fijo + zonas actuales;
- bloqueo de copas y descenso por Anual cuando falla.

### Promedios

- nombres normalizados;
- coherencia de puntos y PJ;
- temporada actual incluida;
- tratamiento explícito de ascendidos;
- bloqueo específico del dominio descenso.

## Garantía conservadora

La función histórica descuenta capacidad conjunta en cruces entre rivales y es segura: puede sobreestimar el puntaje requerido, pero no debería prometer una clasificación falsa.

Su salida debe redactarse así:

> Con X entra seguro. Es una garantía conservadora; el mínimo exacto puede ser menor.

## Escalera exacta

El nuevo motor formula los resultados pendientes como un problema de optimización lineal entera:

- cada partido adopta una y solo una salida;
- el puntaje final del equipo se fija en un valor alcanzable;
- se pregunta si existe un escenario de clasificación;
- se pregunta si existe un escenario de eliminación.

De esa forma se obtiene:

- mínimo todavía posible;
- puntajes condicionados;
- primera garantía matemática;
- ejemplos de resultados compatibles.

En igualdad de puntos se modelan extremos favorables y adversos. No se inventan marcadores, fair play ni sorteos.

## Ventanas con postergados

La previa ya no descarta el segundo encuentro de un equipo. La ventana puede analizar:

- fecha oficial;
- solo postergados;
- fecha más postergados.

Si el equipo consultado juega dos veces, su rango de puntos incorpora ambos partidos.

## Simulación

“Qué le conviene” es estimado. Para cada partido compara tres mundos condicionados con una semilla compartida. La salida incluye cambio en puntos porcentuales y un umbral de ruido.

La fuerza temprana se regulariza para no convertir dos derrotas en una proyección de cero puntos al final.

## Tests

Comandos:

```bash
python -m py_compile calculadora_futbol_argentino.py lpf_models.py lpf_data_quality.py lpf_scenarios.py lpf_exact.py
python -m pytest -q
```

Cobertura incorporada:

- invariantes del núcleo exacto;
- postergado con una fecha posterior ya disputada;
- Anual = Apertura + zona;
- derivación de Apertura;
- bloqueo de Anual vieja;
- escalera condicionada y garantizada;
- ventana con dos partidos del mismo equipo.

## Límites

- Fair play y sorteo requieren datos adicionales.
- La diferencia de gol futura no se anticipa sin simular marcadores.
- La simulación no incorpora lesiones, suspensiones ni mercado.
- El optimizador exacto necesita SciPy.
- La interfaz Streamlit debe verificarse en un entorno con sus dependencias instaladas; los módulos y el flujo principal pueden probarse sin navegador.

## Control agregado en v3.3: cupos móviles

La clasificación internacional no debe tratar la posición actual de la Tabla General como una lista definitiva. La identidad de los campeones puede excluir equipos de la carrera por tabla y correr los cortes.

La aplicación ahora distingue:

- corrimiento por un campeón ubicado en zona de copa;
- plaza adicional por duplicación Apertura-Clausura;
- sucesión interna de Copa Argentina cuando ARGENTINA 3 no puede quedar en el campeón;
- corrimiento de la línea de Sudamericana por equipos que pasan a Libertadores.

La lista de equipos vivos de Copa Argentina tiene fecha y fuente visibles. Si está desactualizada, la explicación debe considerarse provisional.

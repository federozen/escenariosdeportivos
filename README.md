# Calculadora del Fútbol Argentino · LPF 2026

Herramienta Streamlit para una redacción deportiva. Organiza en un mismo flujo las cuentas exactas, las probabilidades estimadas, las previas, el post-resultados y el texto listo para publicar.

## Ejecutar

```powershell
pip install -r requirements.txt
streamlit run calculadora_futbol_argentino.py
```

En el primer ingreso, `Cargar TODO` abre la foto offline incluida. Después se puede actualizar desde ESPN, pegar tablas manuales o cargar marcadores desde la pestaña **Cargar resultados**.

## Flujo recomendado

1. Cargar o actualizar las dos zonas, la Tabla Anual, los promedios y los resultados.
2. Abrir **Mesa de redacción**.
3. Elegir equipo, objetivo y modo `Previa` o `Post`.
4. Copiar el informe exacto y, si hace falta, activar el bloque estimado.
5. Tras cada partido, marcar `Final`, cargar el marcador y tocar **Aplicar y recalcular**.

El chat anterior sigue disponible como **Chat avanzado**.

## Qué es exacto y qué es estimado

- **Exacto:** puntos actuales, techo, piso seguro, línea de clasificación, rango de puesto de una fecha, reparto reglamentario de plazas y reasignación del descenso.
- **Estimado:** probabilidades Monte Carlo, impacto de “la otra cancha”, proyección y árbol probabilístico.

Los dos bloques nunca comparten números sin rótulo. Un modelo de lenguaje opcional puede interpretar una consulta, pero no calcula cifras.

## Arquitectura

- `calculadora_futbol_argentino.py`: interfaz, parsers, datos offline, narrativa y simulación.
- `lpf_exact.py`: núcleo aislado, determinístico y sin dependencia de Streamlit.
- `tests/test_lpf_exact.py`: fuerza bruta y pruebas de invariantes del núcleo sensible.
- `AUDITORIA.md`: reglas confirmadas, correcciones y límites conocidos.

## Despliegue

No requiere base de datos, Graphviz del sistema, un servicio pago ni dependencias gráficas adicionales. `st.graphviz_chart`, `st.dataframe` y los gráficos nativos de Streamlit mantienen el despliegue compatible con Streamlit Community Cloud.

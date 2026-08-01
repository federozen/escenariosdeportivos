# Arquitectura de la versión 3

## Principio

Una cuenta se genera una sola vez y después puede representarse como texto, tabla, gráfico o respuesta de chat. La interfaz no debe recalcular números.

## Flujo de datos

```text
Fuentes / carga manual
        ↓
Normalización y aliases
        ↓
Reconciliación de fixture y resultados
        ↓
Auditoría de Zonas / Anual / Promedios
        ↓
Estado LPF coherente
        ↓
Motor determinístico / optimizador / simulación
        ↓
Explorador · Informes · Visualizaciones · Chat
```

## Módulos

### `lpf_models.py`

Contiene los contratos estructurados:

- `AuditIssue`
- `AuditMetadata`
- `MatchRecord`
- `PointLadderRow`
- `ObjectiveAnalysis`
- `MatchResultScenario`
- `RoundPreview`
- `DataQualityReport`

### `lpf_data_quality.py`

Responsable de:

- normalizar filas;
- validar cantidad de clubes, PJ, puntos y DG;
- reconciliar fixture y resultados;
- identificar partidos pendientes;
- reconstruir la foto fija del Apertura;
- calcular Anual = Apertura + zona actual;
- controlar Promedios;
- bloquear dominios inconsistentes.

Los resultados explícitos son autoritativos. Los PJ solo se usan como inferencia de respaldo y esa inferencia queda visible.

### `lpf_scenarios.py`

Motor MILP para preguntas existenciales:

- ¿puede clasificar con X puntos?;
- ¿puede quedar afuera con X?;
- ¿cuál es su mejor y peor puesto?;
- ¿cuál es el mínimo todavía posible?;
- ¿desde qué puntaje está garantizado?;
- ¿qué pasa si gana, empata o pierde en una ventana con postergados?

Cada partido tiene exactamente una salida entre local, empate y visitante. El optimizador no inventa marcadores ni resuelve criterios no cargados.

### `lpf_exact.py`

Mantiene funciones determinísticas previas y la cota segura para ventanas grandes. Esa cota es conservadora y no se presenta como mínimo exacto.

### `calculadora_futbol_argentino.py`

Conserva la interfaz y la compatibilidad del proyecto original. La nueva capa se integra mediante:

- `_lpf_rebuild_state`
- `_lpf_domain_ready`
- `_lpf_data_gate`
- `render_data_audit`
- `render_guided_workspace`
- `render_visualizations_workspace`
- `render_definition_radar`

## Tabla Anual

La fuente preferida es una foto fija y validada del Apertura. Cada modificación del Clausura recalcula la Tabla Anual automáticamente.

La Anual directa se admite únicamente si:

- contiene los mismos 30 equipos;
- su diferencia de PJ respecto de la zona es coherente;
- sus puntos y estadísticas son posibles;
- no contradice la foto del Apertura.

## Promedios

Se valida:

- presencia de los equipos;
- partidos computados;
- puntos históricos;
- coherencia con la temporada actual;
- tratamiento de recién ascendidos.

Una falla de Promedios bloquea el descenso por Promedios, pero no necesariamente los playoffs.

## Escalabilidad

El optimizador exacto se usa editorialmente en la definición. Para horizontes grandes se evita forzar una enumeración o explicación inmanejable. La UI cambia de estrategia:

- más de seis fechas: garantía conservadora y simulación;
- seis a cuatro: Radar y escalera exacta;
- tres a dos: escenarios reducidos;
- una: árbol exhaustivo, sujeto a los desempates disponibles.

## Capa de narrativas de competencia (v3.3)

`lpf_competition_narratives.py` contiene renderizadores puros de Markdown para:

- zonas;
- Libertadores;
- Sudamericana;
- descenso.

No usa Streamlit ni consulta fuentes externas. Recibe datos ya validados y evita que el Chat, la Mesa y Visualizaciones redacten versiones distintas de la misma situación.

La información cambiante de Copa Argentina se guarda en el estado LPF con:

- `copa_arg_vivos`;
- `copa_arg_updated`;
- `copa_arg_source`;
- `copa_arg_reemplazo`.

ESPN es un proveedor de cotejo. El usuario conserva la posibilidad de carga manual y la aplicación no reemplaza la foto vigente si la respuesta externa es incompleta.

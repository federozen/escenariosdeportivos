# Auditoría comparativa: Calculadora del Fútbol Argentino y Calculadora del Mundial

**Fecha:** 1 de agosto de 2026  
**Alcance:** auditoría sin modificar el código original.

## 1. Conclusión ejecutiva

La herramienta del fútbol argentino no necesita sumar indiscriminadamente funciones del proyecto del Mundial: **ya contiene las 53 funciones principales de ese proyecto**, además de unas 200 funciones nuevas para LPF, copas, descenso, datos, chat y redacción.

El salto de calidad debe concentrarse en cinco cambios:

1. Separar cálculo, datos, narrativa, chat y visualizaciones.
2. Reemplazar el concepto único de “piso” por varias líneas bien definidas.
3. Incorporar un motor exacto de escenarios condicionados para el tramo final.
4. Reconstruir la capa de datos para manejar partidos postergados por identidad y estado, no por cantidad de PJ.
5. Hacer que chat, informes y visualizaciones consuman el mismo objeto de análisis.

La arquitectura recomendada es **mantener Python y Streamlit, pero convertir el proyecto en una aplicación multipágina y modular**, con un motor independiente. No recomiendo separar todavía un backend y un frontend: agregaría complejidad antes de estabilizar los cálculos y los datos.

---

## 2. Estado de los proyectos

### Herramienta del fútbol argentino

- Archivo principal: `calculadora_futbol_argentino.py`.
- Tamaño: 7.383 líneas.
- Funciones: 262.
- Clases o modelos de dominio: 0.
- Referencias a `st.session_state`: 201.
- Llamadas de interfaz `st.*`: aproximadamente 485.
- Núcleo aislado: `lpf_exact.py`, con solo dos funciones públicas sensibles.
- Tests: cuatro pruebas en `tests/test_lpf_exact.py`.
- Documentación: README, auditoría previa y prompt.

Funciones más extensas:

- `ejecutar_accion`: 282 líneas.
- `render_newsroom`: 248 líneas.
- `_router_lpf`: 209 líneas.
- `_parse_kw`: 126 líneas.
- `lpf_previa_equipo_texto`: 114 líneas.

Esto confirma que el proyecto es todavía un monolito: el motor, la carga, el estado, el router, la redacción y la interfaz están fuertemente acoplados.

### Calculadora del Mundial

- Archivo principal: `calculadora_mundial.py`.
- Tamaño: 1.069 líneas.
- Funciones: 56.
- Clases o modelos de dominio: 0.
- Tests automatizados: no tiene.
- Fuente externa opcional: football-data.org.
- Motor principal: enumeración de marcadores cuando quedan pocos partidos y enumeración por G/E/P cuando quedan más.

### Relación entre ambos

Los 53 símbolos funcionales principales del proyecto del Mundial están presentes también en la herramienta argentina. Por lo tanto, el proyecto argentino es una evolución directa del primero.

La adopción no debe consistir en volver a copiar funciones. Debe consistir en:

- rescatar los buenos flujos del Mundial;
- adaptarlos al formato LPF;
- moverlos a un motor común;
- corregir sus limitaciones matemáticas;
- integrarlos en la Mesa de redacción y no dejarlos aislados en el “Chat avanzado”.

---

## 3. Verificaciones realizadas

### Tests y sintaxis

- `python -m pytest -q`: **4 tests aprobados**.
- `py_compile` del proyecto argentino: aprobado.
- `py_compile` del proyecto del Mundial: aprobado.

### Ejecución visual

No fue posible ejecutar Streamlit en este entorno porque el paquete no está instalado y el índice de paquetes disponible no permitió instalarlo. Por eso la auditoría de interfaz se hizo por inspección estática del código. El motor aislado sí pudo ejecutarse y probarse.

### Cobertura actual

Las cuatro pruebas verifican:

- que la garantía conservadora nunca sea menor que el máximo exacto en tres ejemplos pequeños;
- que descuente un enfrentamiento interno;
- que el rango de una fecha respete un cruce entre rivales;
- que un equipo desconocido devuelva `None`.

Es una base correcta, pero insuficiente para un proyecto que calcula copas, descenso, postergados, simulaciones y narrativas publicables.

---

## 4. Hallazgo principal: el “piso seguro” no es siempre el mínimo exacto

La función `safe_guarantee_line` está documentada correctamente en el núcleo: es una **cota segura conservadora**. Puede pedir puntos de más.

Sin embargo, los textos publicables dicen:

> “El equipo que quede 8º puede terminar como mucho con X puntos”.

Esa frase presenta la cota como si fuera el máximo exacto del octavo. No siempre lo es.

### Contraejemplo encontrado durante esta auditoría

En un torneo pequeño con cinco equipos:

- puntos: X 7, A 6, B 4, C 8, D 3;
- objetivo: que X quede por encima de al menos tres rivales;
- máximo exacto del tercer rival: 12;
- línea devuelta por `safe_guarantee_line`: 13.

La herramienta pediría superar 13 —llegar a 14— aunque superar 12 —llegar a 13— ya garantiza el objetivo.

### Consecuencia editorial

Mientras se use este algoritmo, el texto correcto es:

> “Con 14 tiene una garantía conservadora. El mínimo exacto podría ser menor”.

No debe decir:

> “El tercero puede terminar como máximo con 13”.

### Consecuencia de producto

Hay que distinguir:

1. **Garantía exacta:** demostrada por un motor exhaustivo u optimizador.
2. **Garantía conservadora:** segura, pero puede pedir puntos de más.
3. **Corte estimado:** sale de simulación.
4. **Corte actual:** foto de la tabla.

---

## 5. Nuevo modelo para explicar los puntos necesarios

La herramienta debe dejar de mostrar un único “piso”. Para cada equipo y objetivo debe mostrar cuatro referencias.

| Línea | Pregunta que responde | Tipo |
|---|---|---|
| Corte actual | ¿Cuántos puntos tiene hoy el último clasificado? | Exacto |
| Mínimo todavía posible | ¿Cuál es el menor puntaje con el que existe al menos un escenario de clasificación? | Exacto con solver |
| Corte estimado | ¿Dónde es más probable que termine la línea? | Estimado |
| Garantía matemática | ¿Con cuánto entra sin depender de ningún resultado? | Exacto o conservador, rotulado |

A estas cuatro líneas se agrega una quinta capa:

### Clasificación condicionada

Para cada puntaje inferior a la garantía, indicar:

- si todavía puede clasificar;
- si también existe un escenario en el que queda afuera;
- qué resultados son necesarios;
- cuáles son alternativas;
- si depende del desempate;
- qué partidos no influyen.

Ejemplo editorial:

| Puntaje final | Estado | Condición resumida |
|---:|---|---|
| 32 o más | Clasifica seguro | No depende de nadie |
| 31 | Condicionado | Necesita que X no gane |
| 30 | Condicionado | X debe perder y uno entre Y/Z debe dejar puntos |
| 29 | Posible, muy exigente | Requiere al menos tres resultados favorables |
| 28 | No alcanza | No existe escenario de clasificación |

No debe limitarse a “con menos depende”. Debe explicar **de qué depende**.

---

## 6. Cómo calcular la escalera condicionada

Para un puntaje final `P` del equipo objetivo, el motor debe responder tres consultas:

1. `can_qualify(P)`: existe al menos una combinación en la que clasifica.
2. `can_fail(P)`: existe al menos una combinación en la que queda afuera.
3. `guaranteed(P)`: no existe ninguna combinación en la que quede afuera.

Clasificación:

- `can_qualify=False`: puntaje insuficiente.
- `can_qualify=True` y `can_fail=True`: clasificación condicionada.
- `can_fail=False`: garantía matemática.

### Motor recomendado

Cuando falten seis fechas o menos, usar un optimizador exacto por resultados, preferentemente **OR-Tools CP-SAT**, con fallback al algoritmo conservador actual.

El modelo debe representar por partido una sola opción entre:

- victoria local;
- empate;
- victoria visitante.

Con ese modelo se pueden resolver:

- máximo exacto del equipo de corte;
- mínimo posible de clasificación;
- posibilidad de clasificar con un puntaje fijo;
- posibilidad de quedar afuera con ese mismo puntaje;
- mejor y peor puesto;
- escenarios testigo;
- condiciones mínimas.

Para explicar condiciones se puede aplicar una búsqueda iterativa:

1. encontrar un escenario testigo de clasificación;
2. agrupar los resultados externos relevantes;
3. retirar condiciones una por una;
4. conservar solo las indispensables;
5. buscar escenarios alternativos y presentar “A, o bien B”.

No hace falta enumerar las `3^N` combinaciones.

---

## 7. Problemas matemáticos y conceptuales adicionales

### 7.1 Rango de fecha con postergados

`next_round_rank_bounds` funciona cuando cada equipo juega como máximo una vez. La aplicación reconoce el límite, omite el segundo partido y muestra una advertencia.

Pero después sigue utilizando expresiones cercanas a “rango exacto” dentro de una ventana que incluye postergados. El rango es exacto para el subconjunto elegido, no para toda la ventana.

Solución:

- modo `official_round`: exacto para la fecha oficial;
- modo `postponed_only`: exacto para los postergados;
- modo `extended_window`: solver que incluya todos los encuentros, incluso dos por equipo;
- si no hay solver, mostrar los dos tramos por separado.

### 7.2 Equipo que no juega

La función `next_round_rank_bounds` supone que el equipo objetivo puede sumar tres puntos. En una prueba aleatoria donde el objetivo no jugaba, devolvió mejor puesto 4º cuando el resultado exhaustivo era 5º.

La función necesita recibir explícitamente el resultado propio o la cantidad de partidos del objetivo en la ventana.

### 7.3 Explicación falsa sobre las victorias

El texto de previa dice:

> “En cada partido alguien gana y suma 3”.

Puede haber empates. La cuenta puede ser correcta, pero la explicación es incorrecta.

Debe decir:

> “Incluso en la combinación más favorable, el reparto inevitable de puntos deja a X rivales por encima”.

### 7.4 “Mejor realista”

El código calcula rivales que podrían igualar al equipo en su mejor puntaje y suma esa cantidad al puesto. No verifica que todos puedan quedar igualados simultáneamente.

Además, “realista” es una categoría probabilística, no exacta.

Reemplazar por:

- mejor puesto con desempates favorables;
- peor puesto entre los empatados;
- mejor puesto sin depender de desempates;
- puesto más probable, solo si sale de simulación.

### 7.5 “Todos siguen con chances matemáticas”

El relato de zona lo afirma cuando el test conservador no detecta clasificados ni eliminados. Que un equipo no esté demostrado como eliminado no prueba que exista un escenario real de clasificación.

Debe usarse un solver de factibilidad o un texto prudente:

> “El motor conservador todavía no marca clasificados ni eliminados”.

### 7.6 Rendimiento del piso en tablas grandes

En una prueba sintética con 30 equipos y nueve rivales relevantes, `safe_guarantee_line` tardó alrededor de 8,6 segundos. El método prueba subconjuntos y puede degradarse en la Tabla Anual.

Se necesita:

- cachear cálculos;
- evitar recalcular desde varios renderizadores;
- usar solver exacto o un algoritmo de poda más eficiente;
- guardar un `calculation_id` compartido por chat, informe y visual.

---

## 8. Auditoría de simulación

### 8.1 El 4% de River puede estar sesgado por la muestra inicial

`_fuerza_lpf` mezcla:

- 70% puntos por partido del Clausura actual;
- 30% forma de los últimos tres partidos disponibles.

Con dos derrotas, ambas medidas son cero. Después el valor se recorta al mínimo 0,4 respecto del promedio. No usa rendimiento previo, Elo ni el Apertura.

Por eso una probabilidad de 4% en la fecha 2 puede ser más una consecuencia del modelo que una lectura razonable de la fuerza de River.

Recomendación:

- modelo neutral para estudiar fixture;
- modelo predictivo con prior histórico;
- regularización equivalente a seis u ocho partidos previos;
- ocultar o advertir probabilidades tempranas si no hay prior.

### 8.2 Desempates simulados

Las simulaciones suman puntos, pero no simulan goles futuros. Usan la diferencia de gol actual como un decimal pequeño y un epsilon para ordenar empates.

Esto sirve como aproximación temprana, pero no debe presentarse como simulación completa del reglamento, especialmente en las últimas fechas.

Opciones:

- simular marcadores con Poisson cuando quedan pocas fechas;
- abrir un intervalo por desempate;
- reportar dos probabilidades: desempate favorable y desfavorable.

### 8.3 Interzonales

En `_sim_zone_pos`, los interzonales no forzados se simulan como partidos contra un rival promedio. No se usa la fuerza real ni la localía del rival interzonal.

La simulación general `_sim_lpf_add` sí recorre los partidos reales y es una base mejor para un motor común.

### 8.4 “Da igual” y ruido

`lpf_otros_resultados_sim` usa un umbral fijo de 1 punto porcentual y lo denomina ruido. No calcula el error estadístico real.

Con 20.000 simulaciones y una probabilidad cercana al 4%, el error Monte Carlo aproximado es mucho menor que un punto porcentual. Otra cosa es la incertidumbre del modelo, que no se resuelve aumentando corridas.

La salida debe separar:

- error Monte Carlo;
- incertidumbre del modelo;
- umbral editorial de relevancia.

También debe decir **puntos porcentuales**, no “pts”.

---

## 9. Auditoría de datos

### 9.1 El problema más serio: pendientes inferidos por PJ

`lpf_pendientes` decide qué partido está jugado según el número de PJ de cada equipo y el orden de su calendario.

Esto falla con un postergado. Ejemplo:

- un equipo jugó las fechas 1 y 3;
- tiene postergada la fecha 2;
- su PJ es 2.

El algoritmo considera jugados sus dos primeros partidos del fixture —fechas 1 y 2— y pendiente el tercero. Es exactamente lo contrario de lo ocurrido.

Los pendientes deben salir de partidos identificados individualmente, con estado y fecha, no de una resta por PJ.

### 9.2 Fuentes actuales

El proyecto puede cargar desde:

- constantes offline;
- ESPN no oficial;
- football-data.org en el modo genérico;
- Wikipedia/HTML;
- Apify;
- JSON;
- texto manual.

Esto ofrece flexibilidad, pero no existe una capa común de proveedores ni procedencia por campo.

### 9.3 Falta de persistencia y trazabilidad

La mayor parte del estado vive en `st.session_state`. No hay:

- base canónica;
- snapshots;
- historial de cambios;
- rollback persistente;
- prioridad formal entre fuentes;
- resolución de conflictos;
- identificadores estables de equipos y partidos.

### Recomendación de datos

Usar SQLite como almacenamiento local principal, con exportación JSON.

Entidades mínimas:

- `competition`;
- `season`;
- `stage`;
- `zone`;
- `team`;
- `team_alias`;
- `round`;
- `match`;
- `match_status`;
- `standing_snapshot`;
- `qualification_rule`;
- `data_source`;
- `import_batch`;
- `manual_override`.

Campos esenciales de partido:

- ID estable;
- fecha original;
- fecha programada actual;
- fecha real de juego;
- jornada original;
- local y visitante por ID;
- estado: programado, en juego, final, postergado, suspendido, cancelado;
- marcador;
- fuente;
- actualización.

Flujo de actualización:

1. obtener datos;
2. normalizar;
3. comparar con el snapshot vigente;
4. mostrar cambios;
5. validar;
6. aplicar;
7. recalcular;
8. permitir rollback.

---

## 10. Qué conviene adoptar del proyecto del Mundial

Estas ideas son buenas y deben integrarse al modo LPF:

### A. Gana, empata o pierde

Es la visual principal para la previa de una fecha. En LPF debe devolver por cada resultado:

- puntos;
- mejor y peor puesto;
- top 8;
- dependencia propia;
- Tabla Anual;
- copas;
- descenso.

### B. Puesto puntual

Preguntas útiles:

- ¿Puede terminar 8º?
- ¿Qué necesita para terminar 8º o mejor?
- ¿Puede quedar entre los cuatro para definir de local?

### C. Constructor “qué pasa si”

Debe fijar resultados y recalcular todos los objetivos desde el mismo motor.

### D. Mejor y peor escenario testigo

No basta con “entre 6º y 12º”. Hay que poder mostrar una combinación concreta que produce cada extremo.

### E. Distribución de puestos

Útil como estimación cuando faltan varias fechas y como enumeración exacta en la última fecha.

### F. Árbol de escenarios

Muy útil con una o dos fechas. No debe utilizarse como árbol genérico cuando faltan catorce partidos.

### G. Torneo completo

Adaptarlo a:

- dos zonas;
- Tabla Anual;
- tabla efectiva de copas;
- cuadro de octavos;
- equipos clasificados y eliminados.

---

## 11. Qué no conviene trasladar sin cambios

### Enumeración limitada de marcadores

El Mundial reduce el máximo de goles para controlar el número de combinaciones. Una enumeración 0–2 no es exhaustiva para diferencia de gol.

### Número mágico por techos independientes

El cálculo original toma el techo individual del rival N. No descuenta correctamente todos los cruces entre rivales.

### Desempate alfabético

Cuando persiste la igualdad, `_resolver` devuelve equipos ordenados alfabéticamente. Eso solo sirve para estabilizar una tabla visual, no para decidir clasificación.

### Poisson manual simple

Puede conservarse como laboratorio, no como probabilidad editorial principal.

### “Qué le conviene” por combinaciones completas

En grupos pequeños es entendible. En LPF conviene medir el impacto marginal de cada partido y mostrar condiciones combinadas solo en el tramo final.

---

## 12. Visualizaciones recomendadas

### En el chat

Una sola visual contextual:

- previa: gana/empata/pierde;
- qué le conviene: barras de impacto;
- ficha: actual–corte–garantía–techo;
- zona: tabla con línea debajo del 8º;
- piso: escalera de puntajes condicionados.

### Espacio independiente de visualizaciones

1. Corte actual, mínimo posible, corte estimado y garantía.
2. Escalera de clasificación por puntaje.
3. Actual–corte–garantía–techo.
4. Rango de puesto según G/E/P.
5. Matriz de las seis fechas restantes.
6. Cruces directos.
7. Distribución de puestos.
8. Evolución del corte.
9. Impacto de otras canchas.
10. Cómo cambia la garantía al fijar resultados.
11. Mejor y peor escenario concreto.
12. Árbol exacto en la última fecha.

### Visual nueva prioritaria: “Cómo puede bajar la línea”

| Resultado fijado | Garantía antes | Garantía después | Efecto |
|---|---:|---:|---:|
| Pierde el 8º | 32 | 31 | -1 |
| Empatan dos rivales directos | 32 | 30 | -2 |
| Ganan ambos perseguidores | 32 | 32 | Sin cambio |

El efecto debe recalcularse; no se puede sumar linealmente.

---

## 13. Estrategia según el horizonte

### Más de seis fechas

- garantía conservadora claramente rotulada;
- corte estimado;
- probabilidad regularizada;
- fixture y dificultad;
- sin árboles extensos.

### Entre seis y cuatro

Activar “Radar de definición”:

- garantía exacta mediante solver;
- escalera condicionada;
- matriz de fixture;
- cruces directos;
- G/E/P de la próxima fecha;
- cómo puede bajar la línea;
- escenarios testigo.

### Tres o dos fechas

- condiciones mínimas exactas;
- árboles reducidos;
- puesto puntual;
- resultados indispensables y alternativos;
- desempates abiertos.

### Última fecha

- árbol exhaustivo por G/E/P;
- marcadores relevantes;
- diferencia de gol;
- escenarios exactos;
- explicación completa de otras canchas.

---

## 14. Arquitectura recomendada

### Opción elegida: Streamlit multipágina con motor desacoplado

Ventajas:

- conserva el entorno actual;
- menor costo de migración;
- permite probar progresivamente;
- suficiente para uso interno y publicaciones;
- evita infraestructura adicional.

Estructura sugerida:

```text
app.py
pages/
  01_centro_situacion.py
  02_chat_editorial.py
  03_informes.py
  04_visualizaciones.py
  05_datos_auditoria.py
football_engine/
  models.py
  standings.py
  qualification.py
  conditional.py
  scenarios.py
  simulation.py
  tiebreakers.py
  competitions/lpf_2026.py
  audit.py
data_layer/
  database.py
  repositories.py
  normalizers.py
  providers/
    base.py
    espn.py
    manual.py
    json_csv.py
renderers/
  chat.py
  reports.py
  visuals.py
  exports.py
tests/
```

### Por qué no separar backend/frontend todavía

El proyecto aún necesita estabilizar:

- modelo de datos;
- motor exacto;
- reglas;
- contratos de salida.

Una API ahora solo trasladaría el monolito a dos repositorios.

---

## 15. Objetos de análisis compartidos

Crear modelos como:

- `AuditMetadata`;
- `DataSnapshot`;
- `ObjectiveAnalysis`;
- `PointsLadder`;
- `ConditionalBand`;
- `MatchResultScenario`;
- `RoundPreview`;
- `OtherMatchImpact`;
- `ZonePlayoffReport`;
- `ScenarioWitness`.

Ejemplo conceptual:

```python
@dataclass
class PointsLadder:
    current_cutoff: int
    minimum_possible: int | None
    projected_low: int | None
    projected_median: int | None
    projected_high: int | None
    safe_guarantee: int
    guarantee_kind: Literal["exact", "conservative"]
    bands: list[ConditionalBand]
```

Chat, informe y visualización deben recibir la misma instancia de `PointsLadder`.

---

## 16. Plan de implementación

### Fase 1: preservar y aislar

- congelar una copia de la versión actual;
- crear tests de regresión con las tablas actuales;
- extraer modelos, reglas y repositorios;
- bloquear cálculos con datos incoherentes;
- eliminar la copia espejo del núcleo cuando el paquete esté estable.

### Fase 2: datos

- SQLite y snapshots;
- IDs de equipos y partidos;
- importación por lotes;
- estados de partido;
- postergados correctos;
- proveedores intercambiables;
- vista previa y rollback.

### Fase 3: motor exacto

- solver CP-SAT;
- garantía exacta;
- mínimo posible;
- escalera condicionada;
- escenarios testigo;
- fecha oficial y ventana extendida.

### Fase 4: simulación

- modelo neutral;
- prior histórico;
- error Monte Carlo;
- incertidumbre del modelo;
- simulación de goles en el tramo final.

### Fase 5: producto editorial

- centro de situación;
- chat contextual;
- informes;
- espacio de visualizaciones;
- Radar de definición;
- exportación HTML/CSV/imagen.

---

## 17. Tests necesarios

### Datos

- partido postergado entre fechas jugadas;
- equipo con dos partidos en la ventana;
- cambio de horario;
- resultado corregido;
- conflicto de fuentes;
- rollback;
- aliases de clubes.

### Motor exacto

- garantía exacta frente a fuerza bruta;
- mínimo posible;
- puntaje condicionado;
- mejor y peor puesto;
- equipo que no juega;
- dos partidos por equipo;
- cruces internos;
- interzonales;
- empate y criterios abiertos.

### Copas

- campeones excluidos;
- campeón repetido Apertura/Clausura;
- Copa Argentina inalterable;
- Tabla Anual general y efectiva;
- Libertadores y Sudamericana.

### Simulación

- semillas reproducibles;
- invariantes de cupos;
- error estándar;
- comparación neutral/predictiva;
- sensibilidad en primeras fechas.

### Producto

- chat, informe y visual con el mismo `calculation_id`;
- bloqueo por datos amarillos o rojos;
- exportación coherente;
- “¿por qué?” explica la respuesta anterior.

---

## 18. Recomendación final

No conviene implementar primero una nueva interfaz. El orden correcto es:

1. modelo de datos y postergados;
2. objetos estructurados;
3. garantía exacta y escalera condicionada;
4. tests;
5. simulación regularizada;
6. chat, informes y visualizaciones.

La idea más importante del proyecto del Mundial es mostrar **escenarios concretos**, no solo un número. La mejora más importante para la herramienta argentina es convertir el “piso” en una explicación completa:

- con cuánto se asegura;
- con cuánto todavía puede entrar;
- qué tiene que pasar en cada nivel;
- qué resultados bajan la línea;
- qué parte es exacta y qué parte es estimada.

# Auditoría de reglas y cálculos · LPF 2026

Fecha de verificación: 31 de julio de 2026.

## Fuentes primarias

- [Reglamento de los Torneos LPF Primera 2026 · Boletín 6818, Complementario 01](https://assets1.afa.com.ar/2026/BOLETINES/Boletin-Resoluciones-6818---Complementario-01---Reglamento-Torneos-LPF-Primera-2026.pdf)
- [Estatuto AFA aprobado por Asamblea Extraordinaria del 28/10/2025 · artículo 93](https://assets1.afa.com.ar/2025/6782-Boletin-x-Asamblea-Extraordinaria-%2828-10-2025%29.pdf)
- [Zonas y formato oficial 2026 · Liga Profesional](https://www.ligaprofesional.ar/?p=75932)

## Reglas incorporadas

| Tema | Regla confirmada | Fuente |
|---|---|---|
| Formato | Dos zonas de 15; 16 fechas; ocho pasan a octavos | arts. 14–17 |
| Desempate de zona | DG, GF, mano a mano, fair play, sorteo | art. 16 |
| Tabla General | Suma de las fases de zonas de Apertura y Clausura | art. 24.1 |
| Descenso | Uno por promedio y uno por Tabla General | Estatuto, art. 93 |
| Coincidencia | El último promedio baja primero; si también es último de la Anual, baja el siguiente peor de la Anual | Estatuto, art. 93 b.2/b.3 |
| Empate por descenso | Partido desempate; no DG | art. 26.2 |
| Libertadores | Campeones de Apertura, Clausura y Copa Argentina, más tres por Tabla General | arts. 27.1–27.6 |
| Campeón repetido | Apertura + Clausura repetido corre una plaza a la Tabla General | art. 27.7 |
| Copa Argentina repetida | La plaza queda en Copa Argentina y pasa al siguiente equipo de Primera mejor ubicado allí | arts. 27.8/27.8.1 |
| Sudamericana | Seis mejores de la Tabla General sin plaza Libertadores | art. 28.1 |

Los ascendidos de 2026 sí aparecen con promedio calculado sobre sus partidos de la temporada en la tabla oficial cargada. El motor admite una ausencia de histórico, pero no presupone que estén exentos.

## Correcciones sobre la versión recibida

1. El preset predeterminado ya no aplica mano a mano primero: usa el orden reglamentario LPF 2026.
2. `_linea_garantia` dejó de elegir sólo los `k` techos más altos. Ahora prueba todos los subconjuntos relevantes y descuenta cada cruce interno.
3. La cota usa déficit de puntos, no “cantidad de triunfos”: así un empate 1–1 en puntos no produce un falso imposible.
4. El rango de una fecha ya no congela la DG actual. Es exacto por puntos y abre el intervalo si el marcador futuro puede cambiar el desempate.
5. Los textos de copas distinguen la plaza repetida de Apertura/Clausura de la plaza inalterable de Copa Argentina.
6. Cambiar el preset de desempate ya no destruye el estado LPF para convertirlo accidentalmente en una liga genérica.
7. La carga rápida actualiza de manera atómica zonas, Anual, promedios derivados, resultados, forma y pendientes; además conserva una tabla `antes/ahora`.

## Piso seguro

Para un objetivo que tolera como máximo `k-1` rivales por encima, se busca la mayor línea `P` que todavía podría alcanzar simultáneamente un conjunto de `k` rivales.

- Techo individual: `puntos + 3 × partidos restantes`.
- En un subconjunto, cada partido entre dos rivales fue contado dos veces en los partidos restantes, pero reparte como máximo tres puntos: la capacidad conjunta resta tres por cada cruce interno.
- Se recorren todos los subconjuntos relevantes. La condición es una relajación necesaria: puede sobreestimar la línea y pedir algún punto de más, pero no subestimarla ni prometer una garantía falsa.
- Para garantizar el lugar sin depender de desempates hay que superar la línea, no sólo igualarla.

La propiedad de seguridad se contrasta contra enumeración exhaustiva de resultados `local/empate/visitante` en fixtures pequeños.

## Rango tras la próxima fecha

La optimización es separable porque cada equipo juega como máximo una vez en la fecha. Cuando dos rivales se enfrentan, se evalúan juntos con los tres resultados posibles; nunca se les asignan simultáneamente tres puntos.

El resultado es un intervalo exacto por puntos. En igualdad de puntos se informa la incertidumbre en lugar de congelar DG/GF: el marcador aún no existe y luego pueden intervenir mano a mano, fair play o sorteo. En descenso, una igualdad decisiva implica partido desempate.

## Monte Carlo e invariantes

La simulación usa el fixture real, fuerza por puntos/partido, forma reciente, localía y probabilidad de empate. Las comparaciones condicionadas reutilizan semilla para reducir ruido.

Invariantes esperados por torneo simulado:

- Playoffs: 16 clasificados, salvo exclusiones reglamentarias por descenso que se informan aparte.
- Libertadores por Tabla General: `n_lib` plazas configuradas.
- Sudamericana: 6 plazas.
- Descenso: 2 equipos distintos después de la reasignación.

## Límites explícitos

- Si falta el campeón o el mejor equipo elegible de Copa Argentina, el reparto definitivo no se puede conocer desde la Tabla General: la interfaz lo advierte y trabaja de modo condicional.
- Fair play y sorteo no están cargados en la foto offline. Una igualdad que llegue a esos criterios queda rotulada como pendiente.
- ESPN no publica una Tabla Anual confiable en el mismo endpoint de las zonas. La Anual se conserva de la carga autoritativa del usuario y se actualiza con los marcadores ingresados.
- La simulación no incorpora lesiones, suspensiones futuras, mercado de pases ni decisiones disciplinarias todavía no publicadas.

## Verificación local

```powershell
python -m unittest discover -s tests -v
python -m py_compile calculadora_futbol_argentino.py lpf_exact.py
```

La app completa también se prueba con `streamlit.testing.v1.AppTest`: carga offline, cuatro pestañas, objetivos Playoffs/Libertadores/Descenso y ausencia de excepciones.

## Iteración 2 · Jornada, postergados, integridad de carga e hitos

### Jornada en juego vs partidos atrasados
Antes, la "próxima fecha" era `min(fecha pendiente)` en cinco puntos del código. Con un
partido postergado de una fecha anterior, la app quedaba clavada en esa fecha y nunca
mostraba la previa de la siguiente.

`lpf_jornada_actual(pend, umbral=0.5, forzar=None)` separa ahora los dos conceptos: una
fecha sigue "en juego" mientras conserve al menos la mitad de sus partidos por jugar; si
sólo le quedan sueltos, esos pendientes son **postergados** y la jornada operativa pasa a
la fecha siguiente. Devuelve `(jornada, juegos, atrasados)`.

- Los postergados **se incluyen** en la previa, en "qué le conviene" y en la carga de
  resultados, marcados como `Postergado F<n>` en columna aparte.
- `lpf_etiqueta_jornada` titula "Fecha 3 (más 2 partidos postergados de la fecha 2)".
- La Mesa de redacción suma un selector **Ver fecha** para forzar cualquier jornada.
- `lpf_equipos_con_atraso` marca a los equipos con partidos pendientes de fechas previas:
  juegan menos que el resto y su posición en la tabla se lee con esa salvedad.

Verificado con fixture real: con 3 postergados de la fecha 2, la jornada pasa a 3, los
3 atrasados quedan listados aparte y la previa por equipo los incorpora al cálculo.

### Integridad de la carga
`lpf_chequeo_datos` valida zonas (30 equipos, 15 por zona), Tabla Anual, promedios,
fixture pendiente, resultados y la coherencia `pj + pendientes = 16` por equipo. La Mesa
de redacción muestra un semáforo permanente: verde con el detalle de lo cargado, o
amarillo enumerando exactamente qué falta y dónde completarlo.

### Detector de hitos
`lpf_estado_hitos` toma una foto **exacta** (in / out / pelea por `_liga_in_out`) de cada
equipo frente a playoffs, Libertadores, Sudamericana y permanencia por la Anual.
`lpf_detectar_hitos` compara la foto previa con la posterior a cada carga de resultados y
emite los hechos nuevos redactados como noticia: aseguró, quedó eliminado, se salvó,
quedó condenado. `lpf_hitos_posibles` anticipa qué se puede definir en la jornada.

Los hitos se apoyan sólo en cuentas exactas, nunca en la simulación, y se muestran
destacados tras "Aplicar y recalcular".

### Límite conocido
El umbral de 0.5 para decidir si una fecha sigue en juego es una heurística. Con una fecha
partida casi por la mitad (por ejemplo 7 de 15 pendientes) conviene usar el selector
manual de fecha.

### Despliegue: copia espejo del núcleo exacto
`calculadora_futbol_argentino.py` importa `lpf_exact.py`. Si ese archivo no está en el
repositorio, el import falla con `ModuleNotFoundError` y la app no levanta. Para que el
despliegue nunca dependa de haber subido los dos archivos, el import está envuelto en un
`try/except ModuleNotFoundError` con una **copia espejo** del núcleo embebida en el propio
archivo. Verificado ejecutando la app en un directorio que sólo contiene el `.py`
principal: arranca y carga sin excepciones.

Lo recomendable sigue siendo subir ambos archivos y mantenerlos sincronizados: la copia
espejo es una red de seguridad, no la fuente de verdad.

### Tabla Anual desactualizada (causa de puestos imposibles)
Un informe mostraba "River puede terminar 2º en la Anual" cuando la tabla real lo hacía
imposible (su techo de la fecha era 32 y tres equipos ya estaban por encima). La cuenta
era correcta: la **Anual cargada estaba vieja**. ESPN no publica una Anual confiable, así
que queda de la última carga autoritativa y se desincroniza de las zonas.

`lpf_chequeo_datos` ahora lo detecta: compara `pj` de la Anual contra `pj` de las zonas
(la diferencia debe ser constante, porque el Apertura ya terminó) y verifica que ningún
equipo tenga menos puntos en la Anual que en su zona. Si algo no cierra, el semáforo pide
actualizarla y avisa que copas y descenso salen mal hasta corregirla.

### Puestos que dependen de un desempate
El mejor puesto de una fecha se calcula por puntos; si el objetivo queda igualado con
otros, el mejor caso asumía implícitamente que ganaba el desempate. Ahora el texto lo
aclara: informa con quién quedaría igualado y cuál es el mejor puesto realista si pierde
esos desempates.

### Reescritura del informe de copas
El informe anterior repetía tres veces la misma lista de rivales ("le queda por jugar",
"⚔️ mano a mano" y "🔑 mano a mano"), abría con la explicación reglamentaria y dejaba la
conclusión perdida en el medio.

Estructura nueva: **titular con la conclusión**, situación en una línea, un bloque por
objetivo (Libertadores y Sudamericana por separado) donde cada cifra viene con su porqué
inmediato ("de dónde sale ese número", "con quién pelea el corte", "el atajo"), los
partidos que restan **una sola vez**, y la letra chica reglamentaria al final.

### Condiciones explícitas en el informe de copas
Además del número, cada objetivo ahora muestra la cuenta y las condiciones concretas:
- La aritmética a la vista: puntos actuales + partidos × 3 = techo.
- Si depende de sí mismo: las combinaciones exactas de triunfos y empates que llegan a la
  meta (`_combos_puntos`, verificada: toda combinación cumple `3·G + E = faltan` y
  `G + E ≤ partidos`), señalando si hay una sola forma posible o margen de error.
- Si no le alcanza solo: cuántos puntos le faltan que "ya no existen", qué rivales pueden
  superar su techo y **cuántos de ellos** tienen que quedarse cortos para que entre.

### Molde único para los tres informes
Playoffs, copas y descenso comparten ahora la misma estructura, construida por
`_copas_bloque_objetivo(..., modo)`:

1. **Titular** con la conclusión (depende de sí mismo / no le alcanza solo / ya está / afuera).
2. **Situación** en una línea: puesto, puntos, partidos restantes y techo.
3. **Un bloque por objetivo** con la cuenta a la vista, las condiciones concretas
   (combinaciones de triunfos y empates, o cuántos rivales deben quedarse cortos),
   de dónde sale la meta, con quién pelea el corte y el atajo del mano a mano.
4. **Los partidos que le quedan**, una sola vez.
5. **Letra chica** reglamentaria al final.

El parámetro `modo` cambia sólo el lenguaje ("entra" para playoffs y copas, "se salva"
para descenso), sin tocar el cálculo. El informe de descenso separa además **Vía 1
(Tabla General)** y **Vía 2 (Promedios)**, y aclara que basta caer en una para descender.

### Doble conteo al incluir partidos postergados (corregido)
`next_round_rank_bounds` es separable porque asume que **cada equipo juega a lo sumo una
vez** en la ventana. Al incorporar los postergados a la lista de partidos, un equipo que
jugaba en la jornada y además tenía un atrasado se contaba dos veces y el puesto se iba
de rango (se llegó a mostrar "17º" en una zona de 15 equipos).

Corrección: para el rango de puestos se usa un partido por equipo (la jornada, más los
postergados de equipos que no juegan en ella). Los equipos que juegan dos veces se listan
aparte, advirtiendo que pueden sumar hasta 3 puntos más de lo que refleja el rango.

Además, `_rango_puesto_fecha` acota el resultado a `1..N`: un puesto fuera de rango es
siempre un síntoma de doble conteo y ya no puede llegar a pantalla.

### Verificación del "mejor puesto" y detección de Anual desactualizada
Un usuario reportó como error que River figurara con mejor puesto 4º en su zona. Se
verificó por **fuerza bruta** (enumeración completa de los resultados de la fecha): 4º es
correcto. River llega como máximo a 3 puntos y, en cada partido entre sus rivales, alguien
gana y supera ese tope — incluso un equipo con 1 punto que gane llega a 4. El informe lo
explica ahora de forma explícita ("por qué no puede ser 1º esta fecha").

El "2º en la Tabla Anual" del mismo informe **sí era un problema de datos**: la Anual
cargada tenía 17 partidos por equipo cuando las zonas ya reflejaban la fecha 2. El chequeo
de integridad se endureció: como la Anual es Apertura (terminado) + Clausura, la resta
`anual_pj - zona_pj` debe ser **idéntica para los 30 equipos**; cualquier variación implica
que la Anual no incorporó resultados y se avisa nombrando los equipos afectados.

### La Tabla Anual pasa a ser DERIVADA (cambio estructural)
Origen del problema: la Anual se guardaba como una foto independiente (`anual_directo`).
Al actualizar las zonas, esa foto quedaba vieja y las cuentas de copas y descenso salían
mal aunque las fórmulas fueran correctas (caso reportado: "River puede terminar 2º en la
Anual", imposible con la tabla real).

Ahora se guarda la tabla del **Apertura**, que ya terminó y es fija (16 fechas), y la
Anual se calcula siempre como **Apertura + zonas actuales**. Actualizando las zonas, la
Anual se actualiza sola y la desincronización deja de ser posible.

`lpf_apertura_desde_anual` deriva el Apertura restando a la Anual únicamente los partidos
de Clausura que ésta ya incorporaba (`anual_pj - 16`), tomados de los resultados
conocidos. Verificado: los 30 equipos quedan con 16 partidos de Apertura, sin dudosos, y
al cargar una zona actualizada la Anual reproduce los puntos reales.

Consecuencia práctica: para tener números confiables alcanza con mantener **las dos zonas**
al día; la Anual ya no se carga por separado.

### Todos los cargadores derivan la Anual (cierre del problema)
Aunque `Cargar TODO` ya derivaba la Anual, los demás caminos la volvían a congelar con la
constante interna: el botón de zonas, la carga desde ESPN, la carga manual y —el más
dañino— `_rd_apply_results`, que tras cada aplicación de resultados fijaba
`anual_directo` con la foto anterior. Por eso actualizar datos "no cambiaba nada".

Los cuatro pasan ahora a dejar `anual_directo` vacío y a guardar el Apertura, de modo que
la Anual se recalcula siempre desde las zonas vigentes. Verificado: aplicando los
resultados de una fecha, la Anual se mueve sola (Independiente Rivadavia 35 → 38, que es
el valor real) sin pegar ninguna tabla.

Si el usuario pega una Anual explícita, esa se respeta: la derivación sólo actúa cuando
no hay una tabla cargada a mano.

### Vuelta atrás de la Anual derivada
La derivación (Anual = Apertura + zonas) resultó frágil: al reconstruir el Apertura
restando resultados de una Anual que ya venía desincronizada, se generaron tablas con
valores imposibles (Argentinos con 19 PJ cuando el máximo eran 18). El resultado fue peor
que el problema original.

Se volvió al comportamiento predecible: **la Anual cargada se usa tal cual**, sin
aritmética intermedia. Lo que se conserva de aquel intento es la validación: el chequeo
de integridad exige ahora el invariante exacto `anual_pj = 16 + zona_pj` por equipo y
nombra a los que no lo cumplen, de modo que una tabla incoherente se detecta antes de
llegar a los informes.

Lección: con datos de entrada poco confiables, reconstruir tablas por resta introduce más
errores de los que evita. Es preferible exigir el dato correcto y validarlo con dureza.

### Dos errores detectados en una auditoría externa (corregidos)

**1. Faltaba el tercer criterio de desempate.** Las posiciones se ordenaban por puntos y
diferencia de gol, sin **goles a favor**. Con River y Sarmiento ambos en 0 puntos y DG -2,
Sarmiento queda arriba por sus 4 goles a favor: River es 15º, no 14º. El orden
`(pts, DG, GF)` se aplicó en la previa por equipo, en los informes de playoffs y descenso
y en el panel de control. Verificado con la tabla real: devuelve 15º.

**2. "Única forma de llegar" era incorrecto.** Las combinaciones se calculaban exigiendo
sumar *exactamente* los puntos que faltaban, cuando la meta es un **piso**: superarla
también clasifica. Para 38 en 14 partidos se anunciaba "12 triunfos + 2 empates, sin
margen de error", ocultando que 13 triunfos y una derrota (39) también alcanzan.
`_combos_puntos` ahora resuelve "al menos la meta" y el texto lo aclara, mostrando el
puntaje resultante de cada opción.

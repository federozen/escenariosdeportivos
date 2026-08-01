# Actualización 3.3 · Narrativas de competencia y cupos móviles

## Qué cambia

### Relatos de las zonas

Los relatos de Zona A y Zona B ahora muestran:

- puntos, partidos jugados, diferencia de gol y goles a favor del líder;
- último clasificado y primero afuera con PTS, PJ, DG y GF;
- todos los equipos igualados en la línea del octavo;
- criterio que ordena la igualdad;
- distancia entre líder, corte y último;
- equipos que están a una victoria del corte;
- clasificados y eliminados matemáticos;
- partidos restantes, con advertencia si los postergados generan cargas distintas;
- tabla breve de la foto del corte.

Si los goles a favor no fueron cargados, la narrativa muestra `s/d` en lugar de inventar un cero.

### Nuevos relatos generales

Se incorporaron panoramas narrativos para:

- Copa Libertadores 2027;
- Copa Sudamericana 2027;
- descenso por Tabla General y promedios.

Están disponibles en:

- Panel por equipo → Panorama narrativo de la competencia;
- Resumen completo → Cómo está la competencia;
- Mesa de redacción → Panorama general de la competencia;
- Visualizaciones → Copas y descenso;
- Chat libre con preguntas directas.

### Cupos que se corren

La herramienta diferencia:

- cupos propios de Apertura, Clausura y Copa Argentina;
- cupos repartidos por la Tabla General;
- equipos que hoy entrarían;
- primer equipo que espera;
- condiciones que pueden hacer bajar la línea.

Ejemplos que explica:

- si un equipo que hoy clasifica por tabla gana el Clausura, deja ese lugar y entra el siguiente elegible;
- si gana la Copa Argentina, ocurre el mismo corrimiento cuando no tenía ya una plaza propia;
- si el campeón del Apertura también gana el Clausura, se habilita un lugar adicional por la Tabla General;
- si el campeón de Copa Argentina ya era campeón de Apertura o Clausura, ARGENTINA 3 se hereda dentro de la Copa Argentina, no automáticamente por la Anual.

### Seguimiento de la Copa Argentina

Datos y auditoría incorpora:

- listado editable de los equipos que siguen en competencia;
- foto inicial del cuadro de octavos 2026;
- botón para cotejar partidos pendientes con ESPN;
- enlaces al fixture oficial y al cuadro de ESPN;
- fecha y fuente de la foto utilizada;
- campo para cargar al mejor equipo de Primera de Copa Argentina si debe heredar ARGENTINA 3.

ESPN funciona como cotejo. Si devuelve una fase incompleta, la aplicación no reemplaza la lista vigente.

### Descenso

El panorama de descenso muestra:

- último de la Tabla General con PTS, PJ, DG y GF;
- diferencia con el equipo inmediato;
- último y anteúltimo de Promedios;
- coeficiente, puntos, partidos, piso y techo;
- quiénes bajarían si terminara hoy;
- qué ocurre si el mismo equipo es último en ambas tablas;
- aclaración de que un empate en una posición de descenso se define por partido desempate, no por DG.

## Navegación

El Panel por equipo sigue siendo la entrada recomendada. La nueva opción **Panorama narrativo de la competencia** evita que el periodista tenga que recordar preguntas del chat.

El chat también muestra accesos rápidos para:

- cómo está la Libertadores;
- cómo está la Sudamericana;
- cómo está el descenso;
- cómo viene la zona del equipo elegido.

## Verificación

- Compilación Python aprobada.
- 21 tests automatizados aprobados.
- Smoke test de carga de la aplicación con Streamlit simulado aprobado.
- Prueba de reasignación de Copa Argentina aprobada.

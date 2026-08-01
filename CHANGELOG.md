## 3.4

- Agregó un pantallazo narrativo de la fecha completa dentro de **Mesa de redacción → Previa de la fecha**.
- Incorporó el selector **Toda la fecha / Un partido**.
- La vista general resume ambas zonas y luego recorre todos los encuentros con contexto de tabla y rango de puestos.
- La vista por partido agrega ramas exactas gana/empata/pierde para los dos equipos.
- Los postergados quedan marcados con su fecha original.
- Si un equipo juega dos veces en la ventana, la vista general evita mostrar un rango simplificado engañoso; la vista individual usa el motor exacto.
- Las probabilidades se mantienen como bloque estimado separado.
- Total de la entrega: 23 tests automatizados aprobados.

## 3.3

- Mejoró la narrativa de Zona A y Zona B con PJ, DG, GF, igualdad del corte, distancias y tabla breve.
- Agregó relatos generales de Libertadores, Sudamericana y descenso.
- Incorporó explicación dinámica de cupos que se corren por campeones futuros.
- Sumó seguimiento de equipos vivos en Copa Argentina con lista manual, foto de octavos y cotejo ESPN.
- Sumó el reemplazo reglamentario de ARGENTINA 3 dentro de Copa Argentina.
- Incorporó las narrativas al Panel, Mesa de redacción, Visualizaciones y Chat.
- Amplió a 21 tests automatizados.

# Changelog

## 3.0.0 · 2026-08-01

### Base y auditoría

- Se agregó un constructor único de estado LPF.
- Las Zonas, la Tabla Anual, los Promedios, el fixture y los resultados se validan antes de publicar cuentas.
- La Tabla Anual se deriva de una foto fija del Apertura más las zonas actuales cuando esa foto es confiable.
- La Anual directa queda como alternativa únicamente si supera los controles.
- Los cálculos afectados se bloquean por dominio: playoffs, copas, promedios o descenso.
- Se incorporó un semáforo de calidad y un respaldo JSON desde la interfaz.
- Los partidos pasaron a tener identidad, jornada original, estado y procedencia.
- Se corrigió la inferencia de postergados: jugar una fecha posterior no convierte el partido anterior en jugado.

### Motor matemático

- Se agregó un optimizador exacto basado en `scipy.optimize.milp`.
- Nueva escalera de puntajes con mínimo todavía posible, clasificación condicionada y garantía matemática.
- Nuevos rangos exactos por puntos para ventanas en las que un equipo puede jugar dos veces.
- Se mantiene la garantía conservadora para horizontes grandes y se la rotula correctamente.
- Se eliminaron explicaciones falsas sobre reparto de puntos y marcadores futuros.

### Simulación

- La fortaleza temprana se regulariza con una referencia previa y ya no proyecta automáticamente cero por dos derrotas.
- “Qué le conviene” compara victoria local, empate y victoria visitante con la misma semilla.
- Se muestran cambios en puntos porcentuales, ruido estimado y nivel de impacto.
- Cuando ningún partido mueve la probabilidad de forma apreciable, se muestra una conclusión en lugar de muchas filas “da igual”.

### Experiencia de usuario

- Nuevo **Explorador guiado** para no depender de recordar comandos.
- Nuevo espacio de **Visualizaciones**.
- Nuevo panel de **Datos y auditoría**.
- El Chat queda disponible como modo libre.
- La previa distingue Fecha oficial, solo postergados y ventana completa.
- La ficha de equipo prioriza puesto, distancia al corte, techo, próximos partidos y dificultad editorial.
- Nuevo Radar de definición para las últimas seis fechas.

### Pruebas

- Pruebas de postergados, Tabla Anual derivada, Anual vieja, escalera exacta y ventanas dobles.
- Comparación del optimizador contra enumeración exhaustiva en casos pequeños.
- Total de la entrega: 13 pruebas automatizadas aprobadas.

## 3.1

- Tabla Anual reconstruida siempre desde Apertura fijo + zonas actuales.
- Foto fija del Apertura 2026 incorporada y verificada con los resultados de la primera fecha del Clausura.
- Migración automática de sesiones que conservaban una Tabla Anual vieja.
- La Tabla Anual importada deja de ser una fuente viva y queda como control.
- Advertencias y bloqueos filtrados por objetivo: playoffs, copas y descenso.
- Eliminado el mensaje general que invalidaba playoffs por un problema exclusivo de copas o Promedios.
- Nuevo Panel por equipo con Resumen completo como entrada predeterminada.
- Quince tests automatizados aprobados.

## 3.2

- Nuevo espacio visible **Escenarios** con las funciones adaptadas del proyecto del Mundial.
- Gana / empata / pierde reunido en una vista propia.
- Constructor **Qué pasa si…** para fijar resultados y mantener abiertos los demás partidos.
- Búsqueda de puesto puntual a partir de los puntajes alcanzables.
- Mejor y peor caso concreto con combinaciones de resultados que prueban los extremos.
- Distribución estimada de posiciones separada de los rangos exactos.
- Panel de clasificados, eliminados y equipos en carrera.
- Las mismas herramientas también se abren desde el Panel por equipo.
- Diecisiete tests automatizados aprobados.

# Actualización 3.4 · Narrativa general de la fecha

## Qué se agregó

La pestaña **Mesa de redacción → Previa de la fecha** ahora incluye una narrativa breve y reutilizable para presentar la jornada antes de que empiecen los partidos.

El control **Alcance del relato** permite elegir:

- **Toda la fecha:** abre con un pantallazo de las zonas A y B y luego resume todos los partidos de la ventana.
- **Un partido:** permite seleccionar un encuentro y amplía la explicación con las ramas gana, empata y pierde para ambos equipos.

## Qué cuenta la vista general

Para cada zona muestra líder, último clasificado, primero afuera, puntos y diferencia de gol. Después, para cada partido, informa:

- posición, puntos y diferencia de gol de ambos equipos;
- si es un cruce directo por el corte, un duelo de equipos clasificados, una pelea por acercarse al top 8 o un interzonal;
- el rango de puesto posible al cierre de la ventana para los equipos que juegan una sola vez;
- identificación de los postergados y su fecha original.

La narrativa recuerda que los puntos también alimentan la Tabla Anual y, por lo tanto, después repercuten en copas y descenso.

## Vista de un partido

La selección individual agrega una síntesis exacta por puntos para cada equipo:

- puesto posible si gana;
- puesto posible si empata;
- puesto posible si pierde.

Cuando hay igualdad en puntos, el rango contempla tanto un desempate favorable como uno adverso. No inventa marcadores futuros ni adjudica de antemano diferencia de gol, goles a favor, mano a mano, fair play o sorteo.

## Postergados y ventanas dobles

La fecha operativa puede incluir encuentros postergados de jornadas anteriores. Si un equipo juega dos veces en la misma ventana, la vista general lo indica y evita asignarle un rango rápido pensado para un solo partido. La vista individual sí incorpora ambos encuentros mediante el motor exacto.

## Exacto y estimado

La narrativa de posiciones se mantiene separada del bloque de probabilidades:

- **Rangos y ramas:** exactos por puntos.
- **Probabilidades:** estimación basada en fuerza, forma, localía y probabilidad de empate.

## Validación

Se agregaron pruebas para la narrativa general y la vista por partido. La entrega completa supera **23 tests automatizados**.

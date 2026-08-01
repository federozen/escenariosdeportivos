# Actualización 3.2 · Escenarios visibles

La versión 3.1 contenía parte de las funciones heredadas de la calculadora del Mundial, pero varias estaban escondidas en el chat libre o en bloques heredados que no aparecían en el recorrido principal.

La versión 3.2 agrega un espacio superior llamado **Escenarios** y una entrada equivalente dentro del **Panel por equipo**.

## Funciones visibles

1. **Gana / empata / pierde**
   - Fecha oficial.
   - Solo postergados.
   - Fecha más postergados.

2. **Qué pasa si…**
   - Permite fijar uno o más resultados.
   - Los partidos no seleccionados quedan abiertos.
   - Devuelve puntos posibles y rango exacto de puesto.

3. **Puntaje y puesto**
   - Escalera con mínimo posible, clasificación condicionada y garantía.
   - Búsqueda de un puesto puntual y puntajes con los que puede alcanzarlo.

4. **Mejor y peor caso**
   - Muestra una combinación concreta de resultados que prueba cada extremo.

5. **Distribución**
   - Probabilidad estimada de terminar en cada puesto.
   - Queda separada visualmente de los cálculos exactos.

6. **Clasificados y eliminados**
   - Estado matemático de todos los equipos de la zona.

## Criterio de exactitud

- Rangos, puntajes alcanzables y combinaciones factibles: exactos por puntos.
- Empates en puntos: se abren entre desempate favorable y adverso; no se inventan marcadores.
- Distribución de posiciones: estimación por simulación.

## Pruebas

La entrega pasa 17 tests automatizados, incluidos dos nuevos tests para escenarios parcialmente fijados y para mejor/peor caso concreto.

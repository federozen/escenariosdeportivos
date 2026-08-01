# Actualización 3.5.2 — Chat guiado y buscable

## Objetivo

La versión anterior conservaba el chat abierto, pero muchas capacidades seguían dependiendo de conocer la frase correcta. Esta actualización convierte esa pantalla en un catálogo navegable sin quitar la conversación libre.

## Qué cambia

- El encabezado pasa a **Chat guiado + libre**.
- Se puede elegir un **equipo principal** y otro equipo para las comparaciones.
- Las consultas están agrupadas en:
  - Más usadas.
  - Playoffs.
  - Copas.
  - Descenso.
  - Fecha y escenarios.
  - Equipo y rendimiento.
  - Para redactar.
  - Tablas y visuales.
  - Datos y ayuda.
- Cada función aparece como botón con una explicación breve.
- Al tocar el botón, la pregunta se envía automáticamente al chat y la responde el mismo motor determinístico.
- El buscador encuentra funciones por palabras como `Libertadores`, `promedios`, `previa`, `distribución`, `racha` o `actualizado`.
- Un índice desplegable muestra todas las opciones aunque no estén en la categoría seleccionada.
- El campo de escritura libre sigue disponible para preguntas propias y seguimientos como «¿por qué?» o «¿y si empata?».

## Protección contra regresiones

Se agregó `tests/test_chat_discovery_regression.py`, que controla que se mantengan:

- El explorador guiado.
- El selector de equipos.
- El buscador.
- Las nueve categorías LPF.
- Las funciones críticas de previa, distribución, copas y descenso.
- La entrada libre del chat.

La entrega completa supera 31 pruebas automatizadas.

# Actualización 3.1 — reparación de Tabla Anual y experiencia guiada

## Qué se corrigió

La Tabla Anual ya no se conserva como una copia independiente que el periodista tenga que volver a pegar después de cada fecha.

La fuente autoritativa ahora es:

1. foto fija del Apertura 2026;
2. tabla vigente de la Zona A;
3. tabla vigente de la Zona B.

La aplicación reconstruye automáticamente la Tabla Anual con esas tres piezas. La tabla anual importada queda como control o como fuente para reconstruir el Apertura en otras ediciones.

## Migración de sesiones viejas

Al abrir una sesión creada con la versión anterior, la aplicación:

- recupera la foto fija del Apertura incluida en el proyecto;
- vuelve a sumar las zonas actuales;
- reemplaza la Tabla Anual congelada;
- actualiza la base usada por copas y descenso;
- mantiene los antecedentes de Promedios separados de la temporada actual.

No es necesario volver a pegar la Tabla Anual cada vez que se actualizan las zonas.

## Advertencias por objetivo

Un problema en Promedios ya no invalida un informe de playoffs. Un problema de copas o descenso se muestra como una incidencia de otra área y no como un error general del informe.

Los bloqueos se aplican así:

- zonas o fixture incoherentes: bloquean playoffs;
- Tabla Anual no reconstruible: bloquea copas y descenso;
- antecedentes de Promedios incompletos: bloquea descenso por promedio;
- advertencias no relacionadas: no bloquean el informe actual.

## Nueva entrada principal

El antiguo Explorador guiado se convirtió en **Panel por equipo**.

Se eligen una sola vez:

- equipo;
- objetivo;
- vista.

La vista predeterminada es **Resumen completo**, que reúne ficha, próxima fecha y acceso a la cuenta del objetivo. El chat queda para preguntas excepcionales y seguimientos.

## Verificación

Se agregaron pruebas para comprobar que:

- el Apertura puede reconstruirse desde una Tabla Anual de referencia y los resultados incluidos en esa foto;
- una Tabla Anual importada y vieja no bloquea la aplicación cuando existe una foto fija válida del Apertura;
- al avanzar las zonas, todos los PJ de la Tabla Anual se recalculan correctamente;
- copas y descenso usan la tabla reconstruida, no la importada.

Para aplicar la actualización, cerrar por completo la ventana de Streamlit anterior y ejecutar la nueva carpeta. No alcanza con reemplazar archivos mientras el proceso viejo sigue abierto.

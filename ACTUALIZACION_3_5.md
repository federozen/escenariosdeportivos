# Actualización 3.5 · Copas y descenso dentro de la previa

## Qué se agregó

La pestaña **Mesa de redacción → Previa de la fecha** suma ahora el impacto de cada partido sobre la **Tabla Anual**, la clasificación a **Libertadores y Sudamericana** y las dos vías de **descenso**.

El nuevo selector **Sumar al impacto de la zona** permite activar o desactivar por separado:

- **Copas**.
- **Descenso**.

La narrativa principal de las zonas y el selector **Toda la fecha / Un partido** se mantienen sin cambios.

## Criterio editorial para no sobrecargar

El sistema no agrega información de copas o descenso a todos los equipos por una posibilidad matemática remota.

### Copas

Se muestran los equipos que:

- hoy ocupan un cupo de Libertadores o Sudamericana por la Tabla Anual;
- están cerca de alguna de esas líneas;
- o, cuando quedan seis partidos o menos, permanecen a seis puntos o menos del corte.

El texto informa:

- puesto en la Tabla Anual;
- puesto entre los equipos elegibles, descontando a los que ya tienen plaza;
- cupo que ocuparían hoy;
- distancia al último cupo cuando están afuera;
- rango posible al terminar la ventana.

La vista **Un partido** agrega qué zona de copas puede ocupar el equipo si gana, empata o pierde. Distingue si puede quedar en Libertadores, Sudamericana, dentro o fuera de los puestos internacionales.

## Descenso por Tabla Anual

La capa se limita a los últimos puestos de la Tabla Anual. Para cada equipo relevante muestra:

- posición y puntos;
- distancia al último puesto de salvación o margen sobre la zona roja;
- mejor y peor puesto posible al terminar la ventana;
- en la vista individual, el efecto de ganar, empatar o perder sobre la permanencia anual.

La diferencia de gol no se presenta como criterio definitivo cuando una igualdad en posición de descenso exige partido desempate.

## Descenso por promedios

Solo se muestran los clubes ubicados entre los últimos puestos de la tabla de promedios. El relato informa:

- posición y coeficiente actual;
- diferencia con la zona de descenso o con el último que se salva;
- promedio exacto que tendría después del partido si gana, empata o pierde.

Si el equipo juega dos veces en la misma ventana, el texto aclara que esos tres coeficientes corresponden al primer encuentro, antes del otro pendiente.

Si no hay antecedentes válidos cargados, la previa muestra únicamente la situación por Tabla Anual y lo aclara en pantalla.

## Cupos móviles

Los datos se leen sobre la Tabla Anual vigente y el orden de equipos elegibles. La narrativa recuerda que los campeones que todavía no fueron definidos pueden hacer correr la línea hacia abajo. El bloque por partido se concentra en la vía de clasificación por Tabla Anual; las vías directas por título siguen explicadas en los panoramas generales de copas.

## Validación

La versión compila correctamente y supera **25 pruebas automatizadas**, incluidas pruebas específicas para:

- impacto de copas en la previa;
- filtrado editorial de equipos relevantes;
- descenso por Tabla Anual;
- efecto exacto del resultado sobre el promedio.

"""Narrativas editoriales puras para las competencias LPF 2026.

El modulo no consulta fuentes ni usa Streamlit. Recibe datos ya validados por el
motor y devuelve Markdown. De este modo el chat, los informes y las pantallas
pueden reutilizar exactamente el mismo relato.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence


def _num(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _signed(value: object) -> str:
    return f"{_num(value):+d}"


def ordered_rows(base: Mapping[str, Mapping[str, object]]) -> list[dict[str, object]]:
    # La inserción conserva el orden de la tabla fuente para empates que siguen
    # iguales después de PTS, DG y GF. No inventamos un desempate alfabético.
    source_order = {team: index for index, team in enumerate(base)}
    ordered = sorted(
        base.items(),
        key=lambda item: (
            -_num(item[1].get("pts")),
            -_num(item[1].get("dg")),
            -_num(item[1].get("gf")),
            source_order[item[0]],
        ),
    )
    return [
        {
            "pos": index,
            "team": team,
            "pts": _num(data.get("pts")),
            "pj": _num(data.get("pj")),
            "dg": _num(data.get("dg")),
            "gf": _num(data.get("gf")),
            "gf_known": "gf" in data and data.get("gf") is not None,
            "ga": _num(data.get("ga")),
        }
        for index, (team, data) in enumerate(ordered, 1)
    ]


def _gf(row: Mapping[str, object]) -> str:
    return str(_num(row.get("gf"))) if bool(row.get("gf_known")) else "s/d"


def _pts(value: object) -> str:
    number = _num(value)
    return f"{number} punto" if number == 1 else f"{number} puntos"


def _team_list(items: Sequence[str]) -> str:
    if not items:
        return "—"
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " y " + items[-1]


def _tiebreak_between(above: Mapping[str, object], below: Mapping[str, object]) -> str:
    if _num(above.get("pts")) != _num(below.get("pts")):
        return "puntos"
    if _num(above.get("dg")) != _num(below.get("dg")):
        return "diferencia de gol"
    if bool(above.get("gf_known")) and bool(below.get("gf_known")) and _num(above.get("gf")) != _num(below.get("gf")):
        return "goles a favor"
    return "criterios posteriores no incluidos en esta foto"


def zone_story(
    label: str,
    base: Mapping[str, Mapping[str, object]],
    rest: Mapping[str, int],
    *,
    top_n: int = 8,
    total_rounds: int = 16,
    qualified: Iterable[str] = (),
    eliminated: Iterable[str] = (),
) -> str:
    rows = ordered_rows(base)
    if not rows:
        return f"No hay datos cargados para la Zona {label}."

    cut_index = min(max(1, top_n), len(rows)) - 1
    leader = rows[0]
    cutoff = rows[cut_index]
    first_out = rows[cut_index + 1] if cut_index + 1 < len(rows) else None
    max_played = max((_num(row["pj"]) for row in rows), default=0)
    min_remaining = min((int(rest.get(str(row["team"]), 0)) for row in rows), default=0)
    max_remaining = max((int(rest.get(str(row["team"]), 0)) for row in rows), default=0)

    lines = [f"## Zona {label} — cómo está la carrera por los playoffs"]
    lines.append(
        f"**{leader['team']} lidera** con **{_pts(leader['pts'])}** en {leader['pj']} PJ, "
        f"diferencia de gol **{_signed(leader['dg'])}** y **{_gf(leader)} GF**."
    )

    if first_out:
        lines.append(
            f"El corte está en el **{top_n}º puesto**: **{cutoff['team']}** está adentro con "
            f"**{_pts(cutoff['pts'])}**, DG **{_signed(cutoff['dg'])}** y {_gf(cutoff)} GF. "
            f"El primero afuera es **{first_out['team']}**, también con **{_pts(first_out['pts'])}**, "
            f"DG **{_signed(first_out['dg'])}** y {_gf(first_out)} GF."
        )
    else:
        lines.append(
            f"El último puesto de clasificación es de **{cutoff['team']}**, con {_pts(cutoff['pts'])}."
        )

    tied = [row for row in rows if row["pts"] == cutoff["pts"]]
    if len(tied) > 1:
        tied_text = " · ".join(
            f"{row['pos']}º {row['team']} (DG {_signed(row['dg'])}, {_gf(row)} GF)" for row in tied
        )
        lines.append(
            "**Equipos igualados en los puntos del corte:** " + tied_text + ". "
            "El reglamento aplica primero diferencia de gol y luego goles a favor; si la igualdad persiste, se necesitan los criterios posteriores."
        )
        if first_out:
            deciding = _tiebreak_between(cutoff, first_out)
            if deciding == "criterios posteriores no incluidos en esta foto":
                lines.append(
                    f"Entre **{cutoff['team']}** y **{first_out['team']}** también coinciden PTS, DG y GF. "
                    "La tabla cargada conserva un orden, pero esta narrativa no lo atribuye a un desempate que no fue cargado."
                )
            else:
                lines.append(
                    f"La frontera entre **{cutoff['team']}** y **{first_out['team']}** se decide hoy por **{deciding}**."
                )

    leader_gap = _num(leader["pts"]) - _num(cutoff["pts"])
    bottom = rows[-1]
    bottom_gap = _num(cutoff["pts"]) - _num(bottom["pts"])
    around_cut = [
        str(row["team"])
        for row in rows
        if abs(_num(row["pts"]) - _num(cutoff["pts"])) <= 3
    ]
    lines.append(
        f"Del líder al corte hay **{leader_gap} punto{'s' if leader_gap != 1 else ''}**; "
        f"del corte al último hay **{bottom_gap}**. Hay **{len(around_cut)} equipos** a una victoria o menos "
        f"de la línea: {_team_list(around_cut)}."
    )

    qualified_list = list(qualified)
    eliminated_list = list(eliminated)
    if qualified_list:
        lines.append(f"**Clasificados matemáticamente:** {_team_list(qualified_list)}.")
    if eliminated_list:
        lines.append(f"**Sin chances matemáticas:** {_team_list(eliminated_list)}.")
    if not qualified_list and not eliminated_list:
        lines.append("Todavía no hay clasificados ni eliminados matemáticamente.")

    if min_remaining == max_remaining:
        lines.append(
            f"A cada equipo le quedan **{max_remaining} partidos** y hasta **{3 * max_remaining} puntos**. "
            f"La tabla corresponde a {max_played} partidos jugados como máximo sobre {total_rounds} jornadas oficiales."
        )
    else:
        lines.append(
            f"Por postergados, los equipos no tienen todos la misma carga: les quedan entre "
            f"**{min_remaining} y {max_remaining} partidos**. Por eso la lectura debe hacerse con PJ, techo y fixture, "
            "no solo con la posición actual."
        )

    lines.append("### Foto del corte")
    lines.append("| Referencia | Equipo | PTS | PJ | DG | GF |")
    lines.append("|---|---|---:|---:|---:|---:|")
    lines.append(
        f"| Líder | {leader['team']} | {leader['pts']} | {leader['pj']} | {_signed(leader['dg'])} | {_gf(leader)} |"
    )
    lines.append(
        f"| Último clasificado | {cutoff['team']} | {cutoff['pts']} | {cutoff['pj']} | {_signed(cutoff['dg'])} | {_gf(cutoff)} |"
    )
    if first_out:
        lines.append(
            f"| Primero afuera | {first_out['team']} | {first_out['pts']} | {first_out['pj']} | {_signed(first_out['dg'])} | {_gf(first_out)} |"
        )
    lines.append(
        "_Es una fotografía exacta de la tabla validada. No proyecta dónde terminará el corte ni asigna resultados futuros._"
    )
    return "\n\n".join(lines)


def _effective_order(
    annual: Mapping[str, Mapping[str, object]],
    fixed_qualified: Iterable[str],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = ordered_rows(annual)
    fixed = {team for team in fixed_qualified if team}
    effective = [row for row in rows if row["team"] not in fixed]
    return rows, effective


def libertadores_story(
    annual: Mapping[str, Mapping[str, object]],
    *,
    fixed_qualified: Sequence[str],
    table_slots: int,
    aperture_champion: str = "",
    clausura_champion: str = "",
    copa_argentina_champion: str = "",
    clausura_candidates: Iterable[str] = (),
    copa_argentina_alive: Iterable[str] = (),
    copa_snapshot: str = "",
) -> str:
    rows, effective = _effective_order(annual, fixed_qualified)
    if not effective:
        return "No hay una Tabla Anual válida para narrar la clasificación a la Libertadores."

    table_slots = max(0, int(table_slots))
    qualifiers = effective[:table_slots]
    waiting = effective[table_slots] if len(effective) > table_slots else None
    alive = set(copa_argentina_alive)
    clausura_possible = set(clausura_candidates)

    lines = ["## Copa Libertadores 2027 — cómo está la clasificación"]
    fixed_text = _team_list([team for team in fixed_qualified if team])
    lines.append(
        f"La Libertadores tiene plazas para los campeones y **{table_slots} lugares que hoy reparte la Tabla General**. "
        f"Ya están excluidos de esa carrera por tabla: **{fixed_text}**."
    )

    if qualifiers:
        q_text = " · ".join(
            f"{row['team']} ({row['pts']} pts, DG {_signed(row['dg'])})" for row in qualifiers
        )
        lines.append(f"**Hoy entrarían por la Anual:** {q_text}.")
    if waiting:
        lines.append(
            f"El primero que espera es **{waiting['team']}**, con **{waiting['pts']} puntos**, "
            f"DG **{_signed(waiting['dg'])}** y {_gf(waiting)} GF."
        )

    if qualifiers and waiting:
        cutoff = qualifiers[-1]
        if cutoff["pts"] == waiting["pts"]:
            deciding = _tiebreak_between(cutoff, waiting)
            if deciding == "criterios posteriores no incluidos en esta foto":
                lines.append(
                    f"El último cupo está igualado: **{cutoff['team']}** y **{waiting['team']}** coinciden en PTS, DG y GF. "
                    "El orden exacto requiere los criterios posteriores de la Tabla General."
                )
            else:
                lines.append(
                    f"El último cupo está igualado en puntos: **{cutoff['team']}** se mantiene arriba de "
                    f"**{waiting['team']}** por **{deciding}**."
                )
        else:
            gap = _num(cutoff["pts"]) - _num(waiting["pts"])
            lines.append(
                f"La diferencia entre el último que entra y el primero que espera es de **{gap} punto"
                f"{'s' if gap != 1 else ''}**."
            )

    current_names = [str(row["team"]) for row in qualifiers]
    via_clausura = [team for team in current_names if team in clausura_possible]
    via_copa = [team for team in current_names if team in alive]
    if waiting:
        conditions = []
        if via_clausura:
            conditions.append(
                "uno de los actuales clasificados por tabla gana el Clausura "
                f"({_team_list(via_clausura)})"
            )
        if via_copa:
            conditions.append(
                "uno de ellos gana la Copa Argentina "
                f"({_team_list(via_copa)})"
            )
        if aperture_champion and not clausura_champion:
            conditions.append(
                f"**{aperture_champion}** también gana el Clausura, porque la plaza duplicada corre a la Anual"
            )
        if conditions:
            lines.append(
                f"**Cómo puede entrar el siguiente:** {waiting['team']} tomaría un lugar de Libertadores si "
                + "; o si ".join(conditions)
                + "."
            )

    lines.append("### Cómo se mueve la línea")
    lines.append(
        "- Si un equipo que hoy ocupa uno de los cupos por tabla gana el **Clausura** o la **Copa Argentina**, "
        "sale de la lista de la Anual por tener una plaza propia y entra el siguiente equipo elegible."
    )
    lines.append(
        "- Si el campeón del Apertura también gana el Clausura, se habilita **un lugar adicional por la Tabla General** "
        "(art. 27.7)."
    )
    lines.append(
        "- Si el campeón de la Copa Argentina también fue campeón del Apertura o del Clausura, la plaza de Copa Argentina "
        "**no corre automáticamente a la Anual**: pasa al mejor equipo de Primera de esa Copa (arts. 27.8 y 27.8.1)."
    )

    if alive:
        alive_top = [str(row["team"]) for row in rows if row["team"] in alive]
        lines.append(
            f"**Copa Argentina todavía abierta:** {_team_list(alive_top)} siguen con esa vía entre los clubes de Primera cargados."
        )
        if copa_snapshot:
            lines.append(f"_Estado de Copa Argentina: {copa_snapshot}._")

    lines.append(
        "_La tabla de hoy es una foto provisional: los campeones futuros no agregan siempre un cupo nuevo, pero pueden "
        "cambiar qué equipos se excluyen de la Tabla General y hacer correr la línea hacia abajo._"
    )
    return "\n\n".join(lines)


def sudamericana_story(
    annual: Mapping[str, Mapping[str, object]],
    *,
    fixed_qualified: Sequence[str],
    table_slots_lib: int,
    aperture_champion: str = "",
    clausura_champion: str = "",
    clausura_candidates: Iterable[str] = (),
    copa_argentina_alive: Iterable[str] = (),
    copa_snapshot: str = "",
) -> str:
    rows, effective = _effective_order(annual, fixed_qualified)
    start = max(0, int(table_slots_lib))
    sud = effective[start : start + 6]
    waiting = effective[start + 6] if len(effective) > start + 6 else None
    alive = set(copa_argentina_alive)
    clausura_possible = set(clausura_candidates)

    lines = ["## Copa Sudamericana 2027 — cómo está la clasificación"]
    lines.append(
        "La Sudamericana recibe a los **seis mejores de la Tabla General que no tengan plaza en la Libertadores**. "
        "Por eso su corte depende tanto de los puntos como de quiénes terminen siendo campeones."
    )
    if sud:
        lines.append(
            "**Hoy ocuparían los seis lugares:** "
            + " · ".join(f"{row['team']} ({row['pts']} pts, DG {_signed(row['dg'])})" for row in sud)
            + "."
        )
    if waiting:
        last = sud[-1]
        lines.append(
            f"El último cupo es de **{last['team']}** con **{last['pts']} puntos**, DG **{_signed(last['dg'])}**. "
            f"El primero que espera es **{waiting['team']}** con **{waiting['pts']}**, DG **{_signed(waiting['dg'])}**."
        )
        if last["pts"] == waiting["pts"]:
            deciding = _tiebreak_between(last, waiting)
            if deciding == "criterios posteriores no incluidos en esta foto":
                lines.append(
                    "La frontera coincide en PTS, DG y GF. El orden exacto requiere los criterios posteriores de la Tabla General."
                )
            else:
                lines.append(f"La frontera está igualada en puntos y hoy se decide por **{deciding}**.")

        ahead = [str(row["team"]) for row in effective[: start + 6]]
        potential_clausura = [team for team in ahead if team in clausura_possible]
        potential_copa = [team for team in ahead if team in alive and team != aperture_champion]
        shifts = []
        if potential_clausura:
            shifts.append(f"un club ubicado arriba gana el Clausura ({_team_list(potential_clausura)})")
        if potential_copa:
            shifts.append(f"un club ubicado arriba gana la Copa Argentina ({_team_list(potential_copa)})")
        if aperture_champion and not clausura_champion:
            shifts.append(f"{aperture_champion} repite el título en el Clausura")
        if shifts:
            lines.append(
                f"**Cómo puede bajar la línea:** {waiting['team']} puede entrar si " + "; o si ".join(shifts) + "."
            )

    lines.append("### Qué significa que un campeón ‘libere’ lugar")
    lines.append(
        "Cuando un equipo que está en esta franja consigue una plaza de Libertadores como campeón, deja de ocupar un "
        "lugar de Sudamericana y el siguiente de la Anual avanza. El número total de seis cupos no cambia: cambia la identidad "
        "de los equipos excluidos por estar en Libertadores."
    )
    lines.append(
        "La excepción importante es la duplicación de la Copa Argentina con Apertura o Clausura: esa plaza se hereda dentro "
        "de la Copa Argentina y no se entrega de manera automática al siguiente de la Anual."
    )
    if copa_snapshot:
        lines.append(f"_Estado de Copa Argentina considerado: {copa_snapshot}._")
    return "\n\n".join(lines)


def relegation_story(
    annual: Mapping[str, Mapping[str, object]],
    averages: Sequence[Mapping[str, object]],
    *,
    annual_relegations: int = 1,
    average_relegations: int = 1,
) -> str:
    annual_rows = ordered_rows(annual)
    if not annual_rows:
        return "No hay una Tabla Anual válida para narrar el descenso."
    avg_rows = list(averages)
    lines = ["## Descenso 2026 — cómo está la pelea"]
    lines.append(
        f"Hay **{average_relegations} descenso por promedios** y **{annual_relegations} por la Tabla General**. "
        "Un equipo debe quedar fuera de la última posición en ambas carreras para estar completamente a salvo."
    )

    bottom_annual = annual_rows[-max(5, annual_relegations + 3) :]
    last_annual = annual_rows[-1]
    previous_annual = annual_rows[-2] if len(annual_rows) > 1 else None
    lines.append(
        f"**Tabla General:** hoy el último es **{last_annual['team']}**, con **{last_annual['pts']} puntos** en "
        f"{last_annual['pj']} PJ, DG **{_signed(last_annual['dg'])}** y {_gf(last_annual)} GF."
    )
    if previous_annual:
        gap = _num(previous_annual["pts"]) - _num(last_annual["pts"])
        lines.append(
            f"Está a **{gap} punto{'s' if gap != 1 else ''}** de **{previous_annual['team']}**, que tiene "
            f"{previous_annual['pts']} puntos. La DG se muestra como contexto, pero una igualdad en una posición de descenso "
            "se define mediante partido desempate, no por diferencia de gol."
        )

    if avg_rows:
        last_avg = avg_rows[-1]
        prev_avg = avg_rows[-2] if len(avg_rows) > 1 else None
        lines.append(
            f"**Promedios:** el último es **{last_avg.get('Equipo')}** con **{float(last_avg.get('PROMEDIO', 0)):.3f}**, "
            f"producto de {last_avg.get('Pts', 0)} puntos en {last_avg.get('PJ', 0)} partidos."
        )
        if prev_avg:
            diff = float(prev_avg.get("PROMEDIO", 0)) - float(last_avg.get("PROMEDIO", 0))
            lines.append(
                f"La diferencia con **{prev_avg.get('Equipo')}** es de **{diff:.3f}** en el coeficiente actual. "
                "En esta tabla cada resultado cambia también el denominador, especialmente para los recién ascendidos."
            )

        avg_relegated = [str(row.get("Equipo")) for row in avg_rows[-average_relegations:]]
    else:
        avg_relegated = []
        lines.append("**Promedios:** faltan antecedentes válidos; esta vía debe quedar bloqueada hasta completar la fuente.")

    annual_candidates = [str(row["team"]) for row in annual_rows]
    annual_relegated = [team for team in reversed(annual_candidates) if team not in avg_relegated][:annual_relegations]
    if avg_relegated:
        lines.append(f"**Si terminara hoy, bajaría por promedios:** {_team_list(avg_relegated)}.")
    if annual_relegated:
        lines.append(f"**Y por la Tabla General:** {_team_list(annual_relegated)}.")
    if avg_relegated and str(last_annual["team"]) in avg_relegated:
        lines.append(
            f"**{last_annual['team']} es último en las dos tablas:** descendería por promedios y el descenso de la Anual "
            f"pasaría al siguiente peor equipo que no haya bajado ya por esa vía ({_team_list(annual_relegated)})."
        )

    lines.append("### Los que están hoy en la zona de riesgo")
    lines.append("| Tabla General | PTS | PJ | DG | GF |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in bottom_annual:
        lines.append(
            f"| {row['team']} | {row['pts']} | {row['pj']} | {_signed(row['dg'])} | {_gf(row)} |"
        )
    if avg_rows:
        lines.append("\n| Promedios | Promedio | Pts | PJ | Piso | Techo |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in avg_rows[-5:]:
            lines.append(
                f"| {row.get('Equipo')} | {float(row.get('PROMEDIO', 0)):.3f} | {row.get('Pts', 0)} | "
                f"{row.get('PJ', 0)} | {float(row.get('Piso', 0)):.3f} | {float(row.get('Techo', 0)):.3f} |"
            )
    lines.append(
        "_Es una foto exacta de las tablas cargadas. Los pisos y techos de promedio son rangos matemáticos; no son una "
        "predicción de resultados._"
    )
    return "\n\n".join(lines)

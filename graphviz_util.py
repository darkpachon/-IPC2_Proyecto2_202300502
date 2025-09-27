def generate_tda_dot(greenhouse, tiempo_sec, snapshot=None):
    lines = []
    lines.append("digraph G {")
    lines.append('rankdir=LR; node [shape=record];')

    drones_data = snapshot['drones'] if snapshot else [(d.nombre, d.hilera, d.posicion, d.litros_usados, d.gramos_usados) for d in greenhouse.drones]
    plants_data = snapshot['plants'] if snapshot else [(p.hilera, p.posicion, p.litros, p.gramos, p.regada) for p in greenhouse.plantas]
    plan_data = snapshot['plan'] if snapshot else []

    idx = 0
    for d in drones_data:
        idx += 1
        nombre, hilera, pos, litros, gramos = d
        label = f"{{Dron|Nombre: {nombre}\\nHilera: {hilera}\\nPos: {pos}\\nL: {litros}\\nG: {gramos}}}"
        lines.append(f'drone{idx} [label="{label}"];')

    idxp = 0
    for p in plants_data:
        idxp += 1
        hil, pos, litros, gramos, regada = p
        estado = "REGADA" if regada else "PENDIENTE"
        label = f"{{Planta|H{hil}P{pos}\\nL:{litros}\\nG:{gramos}\\n{estado}}}"
        lines.append(f'plant{idxp} [label="{label}"];')

    if plan_data:
        entry_labels = []
        for e in plan_data:
            hil, pos, done = e
            status = "✓" if done else " "
            entry_labels.append(f"H{hil}P{pos} {status}")
        label = "{Plan|" + "\\n".join(entry_labels) + "}"
        lines.append(f'plan1 [label="{label}"];')

    lines.append("}")
    return "\n".join(lines)

def render_dot_to_png(dot_text, output_path_png):
    try:
        from graphviz import Source
        s = Source(dot_text)
        s.format = 'png'
        s.render(filename=output_path_png, cleanup=True)
        return output_path_png + '.png'
    except Exception:
        return None

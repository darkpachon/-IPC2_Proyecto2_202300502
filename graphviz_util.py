def generate_tda_dot(greenhouse, tiempo_sec, timeline=None):
    lines = []
    lines.append("digraph G {")
    lines.append('rankdir=LR; node [shape=record];')
    drone_nodes = []
    idx = 0
    for d in greenhouse.drones:
        idx += 1
        label = f"{{Dron|Nombre: {d.nombre}\\nHilera: {d.hilera}\\nPos: {d.posicion}\\nL: {d.litros_usados}\\nG: {d.gramos_usados}}}"
        lines.append(f'drone{idx} [label="{label}"];')
        drone_nodes.append(f"drone{idx}")
    idxp = 0
    for p in greenhouse.plantas:
        idxp += 1
        estado = "REGADA" if p.regada else "PENDIENTE"
        label = f"{{Planta|H{p.hilera}P{p.posicion}\\nL:{p.litros}\\nG:{p.gramos}\\n{estado}}}"
        lines.append(f'plant{idxp} [label="{label}"];')
    idxpl = 0
    for plan in greenhouse.planes:
        idxpl += 1
        entry_labels = []
        for e in plan.entries:
            status = "✓" if e.done else " "
            entry_labels.append(f"H{e.hilera}P{e.posicion} {status}")
        label = "{Plan|%s}" % "\\n".join(entry_labels)
        lines.append(f'plan{idxpl} [label="{label}"];')
    for i in range(1, idx):
        if i < idx:
            lines.append(f"drone{i} -> drone{i+1} [style=dotted];")
    for i in range(1, idxp):
        if i < idxp:
            lines.append(f"plant{i} -> plant{i+1} [style=dotted];")
    lines.append("}")
    return "\n".join(lines)

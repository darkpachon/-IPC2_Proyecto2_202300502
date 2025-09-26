import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_output_xml(greenhouses, simulations_by_invernadero, path_out):
    root = ET.Element('datosSalida')
    listaInv = ET.SubElement(root, 'listaInvernaderos')
    for gh, sim_data in simulations_by_invernadero:
        inv_el = ET.SubElement(listaInv, 'invernadero', {'nombre': gh.nombre})
        listaPlanes = ET.SubElement(inv_el, 'listaPlanes')
        for plan, tiempo_opt, eficiencia_ll, timeline in sim_data:
            plan_el = ET.SubElement(listaPlanes, 'plan', {'nombre': plan.nombre})
            ET.SubElement(plan_el, 'tiempoOptimoSegundos').text = str(tiempo_opt)
            total_litros = 0
            total_gramos = 0
            for dn in eficiencia_ll:
                total_litros += dn[1]
                total_gramos += dn[2]
            ET.SubElement(plan_el, 'aguaRequeridaLitros').text = str(total_litros)
            ET.SubElement(plan_el, 'fertilizanteRequeridoGramos').text = str(total_gramos)
            edr = ET.SubElement(plan_el, 'eficienciaDronesRegadores')
            for dn in eficiencia_ll:
                ET.SubElement(edr, 'dron', {
                    'nombre': dn[0],
                    'litrosAgua': str(dn[1]),
                    'gramosFertilizante': str(dn[2])
                })
            instr = ET.SubElement(plan_el, 'instrucciones')
            for seg, acciones_ll in timeline:
                tiempo_el = ET.SubElement(instr, 'tiempo', {'segundos': str(seg)})
                for dn_name, accion in acciones_ll:
                    ET.SubElement(tiempo_el, 'dron', {'nombre': dn_name, 'accion': accion})
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(path_out, 'w', encoding='utf-8') as f:
        f.write(xmlstr)

def generate_html_report(gh, plan, tiempo_opt, eficiencia_ll, timeline, path_html):
    html = []
    html.append("<html><head><meta charset='utf-8'><title>Reporte Invernadero</title></head><body>")
    html.append(f"<h1>Invernadero: {gh.nombre}</h1>")
    html.append(f"<h2>Plan: {plan.nombre}</h2>")
    html.append(f"<p>Tiempo óptimo (segundos): {tiempo_opt}</p>")
    html.append("<h3>Eficiencia por dron</h3>")
    html.append("<table border='1'><tr><th>Dron</th><th>Litros</th><th>Gramos</th></tr>")
    for dn in eficiencia_ll:
        html.append(f"<tr><td>{dn[0]}</td><td>{dn[1]}</td><td>{dn[2]}</td></tr>")
    html.append("</table>")
    html.append("<h3>Instrucciones por segundo</h3>")
    html.append("<table border='1'><tr><th>Segundo</th><th>Acciones</th></tr>")
    for seg, acciones_ll in timeline:
        acciones_text = ", ".join([f"{a[0]}: {a[1]}" for a in acciones_ll])
        html.append(f"<tr><td>{seg}</td><td>{acciones_text}</td></tr>")
    html.append("</table></body></html>")
    with open(path_html, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))

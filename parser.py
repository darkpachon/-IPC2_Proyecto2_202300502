import xml.etree.ElementTree as ET
from models import Greenhouse, Drone, Plant, Plan
def parse_input_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    drones_global = {}
    listaDrones = root.find('listaDrones')
    if listaDrones is not None:
        for d in listaDrones.findall('dron'):
            id_ = d.attrib.get('id')
            nombre = d.attrib.get('nombre')
            drones_global[id_] = Drone(int(id_), nombre)
    invernaderos = []
    listaInvernaderos = root.find('listaInvernaderos')
    if listaInvernaderos is None:
        return []
    for inv in listaInvernaderos.findall('invernadero'):
        nombre = inv.attrib.get('nombre')
        numeroHileras = inv.find('numeroHileras').text.strip()
        plantasXhilera = inv.find('plantasXhilera').text.strip()
        gh = Greenhouse(nombre, numeroHileras, plantasXhilera)
        listaPlantas = inv.find('listaPlantas')
        if listaPlantas is not None:
            for p in listaPlantas.findall('planta'):
                h = p.attrib.get('hilera')
                pos = p.attrib.get('posicion')
                l = p.attrib.get('litrosAgua')
                g = p.attrib.get('gramosFertilizante')
                tipo = (p.text or "").strip()
                plant = Plant(h, pos, l, g, tipo)
                gh.plantas.add_last(plant)
        asign = inv.find('asignacionDrones')
        if asign is not None:
            for a in asign.findall('dron'):
                id_ = a.attrib.get('id')
                hilera = a.attrib.get('hilera')
                if id_ in drones_global:
                    dr = drones_global[id_]
                    dr.hilera = int(hilera)
                    gh.drones.add_last(dr)
        planesRiego = inv.find('planesRiego')
        if planesRiego is not None:
            for pl in planesRiego.findall('plan'):
                nombre_plan = pl.attrib.get('nombre')
                plan_obj = Plan(nombre_plan)
                raw = (pl.text or "").strip()
                if raw:
                    parts = [s.strip() for s in raw.split(',')]
                    for part in parts:
                        if part.startswith('H'):
                            hp = part.replace('H','').split('-P')
                            if len(hp) == 2:
                                plan_obj.add_entry(int(hp[0]), int(hp[1]))
                gh.planes.add_last(plan_obj)
        invernaderos.append(gh)
    return invernaderos

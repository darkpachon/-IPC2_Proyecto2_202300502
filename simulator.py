from tdas import LinkedList

def simulate_plan(greenhouse, plan):
    timeline = LinkedList()
    snapshots = {}  

    total_entries = 0
    for e in plan.entries:
        total_entries += 1
    entries_iter = plan.entries

    def next_pending_entry():
        for entry in entries_iter:
            if not entry.done:
                return entry
        return None

    segundos = 0
    finished_entries = 0
    steps = 0
    max_steps = total_entries * 10  

    while finished_entries < total_entries and steps < max_steps:
        steps += 1
        segundos += 1
        acciones_this_second_ll = LinkedList()
        current_entry = next_pending_entry()
        water_done_this_second = False

        for drone in greenhouse.drones:
            action = "Esperar"
            if (current_entry and drone.hilera == current_entry.hilera 
                and drone.posicion == current_entry.posicion 
                and (not current_entry.done) 
                and (not water_done_this_second)):

                action = "Regar"
                plant = greenhouse.find_plant(current_entry.hilera, current_entry.posicion)
                if plant and not plant.regada:
                    plant.regada = True
                    drone.litros_usados += plant.litros
                    drone.gramos_usados += plant.gramos
                current_entry.done = True
                finished_entries += 1
                water_done_this_second = True

            else:
                target = None
                for e in plan.entries:
                    if not e.done and e.hilera == drone.hilera:
                        target = e
                        break
                if target:
                    if drone.posicion < target.posicion:
                        drone.posicion += 1
                        action = f"Adelante (H{drone.hilera}P{drone.posicion-1})"
                    elif drone.posicion > target.posicion:
                        drone.posicion -= 1
                        action = f"Atras (H{drone.hilera}P{drone.posicion+1})"
                    else:
                        action = "Esperar"
                else:
                    if drone.posicion > 1:
                        drone.posicion -= 1
                        action = f"Atras (H{drone.hilera}P{drone.posicion+1})"
                    else:
                        action = "FIN"

            acciones_this_second_ll.add_last((drone.nombre, action))

        timeline.add_last((segundos, acciones_this_second_ll))

        snapshots[segundos] = {
            'drones': [(d.nombre, d.hilera, d.posicion, d.litros_usados, d.gramos_usados) for d in greenhouse.drones],
            'plants': [(p.hilera, p.posicion, p.litros, p.gramos, p.regada) for p in greenhouse.plantas],
            'plan': [(e.hilera, e.posicion, e.done) for e in plan.entries]
        }

    tiempo_optimo = segundos
    eficiencia = LinkedList()
    for d in greenhouse.drones:
        eficiencia.add_last((d.nombre, d.litros_usados, d.gramos_usados))
    return tiempo_optimo, timeline, eficiencia, snapshots

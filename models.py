from tdas import LinkedList
class Drone:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre
        self.hilera = None
        self.posicion = 1
        self.litros_usados = 0
        self.gramos_usados = 0
        self.finished = False
    def move_towards(self, target_pos):
        if self.posicion < target_pos:
            self.posicion += 1
            return f"Adelante (H{self.hilera}P{self.posicion-1})"
        elif self.posicion > target_pos:
            self.posicion -= 1
            return f"Atras (H{self.hilera}P{self.posicion+1})"
        else:
            return "Esperar"
class Plant:
    def __init__(self, hilera, posicion, litros, gramos, tipo=""):
        self.hilera = int(hilera)
        self.posicion = int(posicion)
        self.litros = float(litros)
        self.gramos = float(gramos)
        self.tipo = tipo
        self.regada = False
class PlanEntry:
    def __init__(self, hilera, posicion):
        self.hilera = int(hilera)
        self.posicion = int(posicion)
        self.done = False
class Plan:
    def __init__(self, nombre):
        self.nombre = nombre
        self.entries = LinkedList()
    def add_entry(self, hilera, posicion):
        self.entries.add_last(PlanEntry(hilera, posicion))
class Greenhouse:
    def __init__(self, nombre, numero_hileras, plantas_por_hilera):
        self.nombre = nombre
        self.numero_hileras = int(numero_hileras)
        self.plantas_por_hilera = int(plantas_por_hilera)
        self.plantas = LinkedList()
        self.drones = LinkedList()
        self.asignaciones = LinkedList()
        self.planes = LinkedList()
    def find_plant(self, hilera, posicion):
        for p in self.plantas:
            if p.hilera == int(hilera) and p.posicion == int(posicion):
                return p
        return None
    def find_drone_by_hilera(self, hilera):
        for d in self.drones:
            if d.hilera == int(hilera):
                return d
        return None

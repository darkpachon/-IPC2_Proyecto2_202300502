from models.tda_lista import ListaEnlazada

class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_por_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_por_hilera = plantas_por_hilera
        self.plantas = ListaEnlazada()
        self.asignacion_drones = ListaEnlazada()
        self.planes_riego = ListaEnlazada()
    
    def agregar_planta(self, planta):
        self.plantas.agregar(planta)
    
    def asignar_dron(self, dron, hilera):
        self.asignacion_drones.agregar({"dron": dron, "hilera": hilera})
    
    def agregar_plan_riego(self, plan):
        self.planes_riego.agregar(plan)
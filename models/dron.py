from models.tda_lista import ListaEnlazada

class Dron:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.hilera_asignada = None
        self.agua_usada = 0
        self.fertilizante_usado = 0
        self.instrucciones = ListaEnlazada()
    
    def agregar_instruccion(self, tiempo, accion):
        self.instrucciones.agregar({"tiempo": tiempo, "accion": accion})
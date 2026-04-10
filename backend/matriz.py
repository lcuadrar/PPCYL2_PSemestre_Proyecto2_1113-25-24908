class Nodo:
    def __init__(self, fila, columna, valor):
        self.fila = fila        # actividad (ej: Tarea1)
        self.columna = columna  # carnet del estudiante
        self.valor = valor      # la nota
        self.siguiente = None   # apunta al siguiente nodo

class MatrizDispersa:
    def __init__(self):
        self.nodos = []  # lista de nodos

    def insertar(self, fila, columna, valor):
        # Si la nota no es válida, no la guardamos
        if valor < 0 or valor > 100:
            return
        nodo = Nodo(fila, columna, valor)
        self.nodos.append(nodo)

    def obtener(self, fila, columna):
        for nodo in self.nodos:
            if nodo.fila == fila and nodo.columna == columna:
                return nodo.valor
        return None  # no existe esa nota
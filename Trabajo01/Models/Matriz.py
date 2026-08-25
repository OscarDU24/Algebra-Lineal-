class Matriz:

    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.valores = []

    def definir_tamano(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

        self.valores = [
            [None for _ in range(columnas)]
            for _ in range(filas)
        ]

    def esta_completa(self):
        if self.filas == 0 or self.columnas == 0:
            return False

        for fila in self.valores:
            if any(valor is None for valor in fila):
                return False

        return True

    def mostrar(self):
        for fila in self.valores:
            print(fila)
# ==========================================================
# CLASE MATRIZ
# Representa la estructura de una matriz mediante una lista
# anidada y almacena su cantidad de filas y columnas.
# ==========================================================

class Matriz:

    # ======================================================
    # CONSTRUCTOR
    # Inicializa una matriz sin tamaño definido.
    # ======================================================
    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.valores = []

    # ======================================================
    # DEFINIR TAMAÑO
    # Crea una matriz vacía utilizando la cantidad de filas
    # y columnas indicada por el usuario.
    # ======================================================
    def definir_tamano(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.valores = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                fila.append(None)
            self.valores.append(fila)

    # ======================================================
    # VALIDAR MATRIZ
    # Comprueba si la matriz ya contiene valores en todas
    # sus posiciones.
    # ======================================================
    def esta_completa(self):
        if self.filas == 0 or self.columnas == 0:
            return False
        for fila in self.valores:
            for valor in fila:
                if valor is None:
                    return False
        return True

    # ======================================================
    # MOSTRAR MATRIZ
    # Recorre las filas de la matriz y muestra sus valores.
    # ======================================================
    def mostrar(self):
        for fila in self.valores:
            print(fila)
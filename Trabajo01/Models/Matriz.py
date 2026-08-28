# ==========================================================
# MODELO DE MATRIZ
# Representa la estructura de una matriz mediante una lista
# de listas. La clase almacena las filas, columnas y valores
# de la matriz.
# ==========================================================

class Matriz:

    # ======================================================
    # CONSTRUCTOR
    # Inicializa una matriz vacía sin dimensiones definidas.
    # ======================================================

    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.valores = []

    # ======================================================
    # DEFINIR TAMAÑO
    # Establece la cantidad de filas y columnas y crea una
    # matriz inicialmente vacía.
    # ======================================================

    def definir_tamano(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.valores = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                fila.append(0)
            self.valores.append(fila)

    # ======================================================
    # INSERTAR VALOR
    # Modifica un elemento específico de la matriz.
    # ======================================================

    def insertar_valor(self, fila, columna, valor):
        self.valores[fila][columna] = valor

    # ======================================================
    # OBTENER VALOR
    # Devuelve el elemento ubicado en una posición específica.
    # ======================================================

    def obtener_valor(self, fila, columna):
        return self.valores[fila][columna]

    # ======================================================
    # VERIFICAR SI LA MATRIZ ESTÁ COMPLETA
    # Comprueba que la matriz tenga las dimensiones definidas
    # y que todos sus elementos hayan sido establecidos.
    # ======================================================

    def esta_completa(self):
        if len(self.valores) != self.filas:
            return False
        for fila in self.valores:
            if len(fila) != self.columnas:
                return False
        return True

    # ======================================================
    # OBTENER COPIA
    # Devuelve una copia independiente de los valores de la
    # matriz.
    # ======================================================

    def obtener_copia(self):
        copia = []
        for fila in self.valores:
            copia.append(fila.copy())
        return copia
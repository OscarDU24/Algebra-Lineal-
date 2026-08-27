# ==========================================================
# CLASE MATRIZ
# Representa la matriz aumentada del sistema de ecuaciones
# mediante una lista anidada. La última columna corresponde
# al vector de términos independientes.
# ==========================================================

class Matriz:
    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.valores = []

    # ======================================================
    # DEFINIR TAMAÑO
    # Crea una matriz vacía con la cantidad de filas y
    # columnas indicada.
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
    # MATRIZ COMPLETA
    # Comprueba si la matriz ya contiene los datos necesarios
    # para trabajar con ella.
    # ======================================================
    def esta_completa(self):
        if self.filas == 0 or self.columnas == 0:
            return False
        return True

    # ======================================================
    # MOSTRAR MATRIZ
    # Muestra la matriz aumentada separando visualmente los
    # coeficientes de los términos independientes.
    # ======================================================
    def mostrar(self):
        if self.filas == 0:
            print("La matriz todavía no ha sido creada.")
            return
        for i in range(self.filas):
            fila = self.valores[i]
            coeficientes = fila[:-1]
            independiente = fila[-1]
            print(f"{coeficientes} | {independiente}")
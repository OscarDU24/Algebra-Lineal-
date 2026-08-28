# ==========================================================
# INTERFAZ DE MATRIZ
# Define las operaciones básicas que debe proporcionar el
# acceso a los datos de una matriz.
# ==========================================================

class InterfazMatriz:

    def guardar(self, matriz):
        raise NotImplementedError

    def obtener(self):
        raise NotImplementedError

    def limpiar(self):
        raise NotImplementedError
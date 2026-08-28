# ==========================================================
# DAO DE MATRIZ
# Se encarga de almacenar y recuperar la información de la
# matriz. No realiza operaciones matemáticas.
# ==========================================================

from Dao.interfaz_matriz import InterfazMatriz

class MatrizDAO(InterfazMatriz):

    # ======================================================
    # CONSTRUCTOR
    # Inicializa el almacenamiento de la matriz.
    # ======================================================

    def __init__(self):
        self.matriz = None

    # ======================================================
    # GUARDAR MATRIZ
    # Almacena una copia de los valores recibidos.
    # ======================================================

    def guardar(self, matriz):
        self.matriz = []
        for fila in matriz:
            self.matriz.append(fila.copy())

    # ======================================================
    # OBTENER MATRIZ
    # Devuelve una copia de la matriz almacenada.
    # ======================================================

    def obtener(self):
        if self.matriz is None:
            return []
        copia = []
        for fila in self.matriz:
            copia.append(fila.copy())
        return copia

    # ======================================================
    # LIMPIAR MATRIZ
    # Elimina la matriz almacenada.
    # ======================================================

    def limpiar(self):
        self.matriz = None
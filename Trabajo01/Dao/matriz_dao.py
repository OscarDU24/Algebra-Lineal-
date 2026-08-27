# ==========================================================
# IMPORTACIÓN DE LA INTERFAZ
# ==========================================================

from Dao.interfaz_matriz import InterfazMatriz

# ==========================================================
# CLASE MATRIZ DAO
# Se encarga de insertar y consultar los valores almacenados
# en la matriz.
# ==========================================================

class MatrizDAO(InterfazMatriz):
    def insertar_valor(self, matriz, fila, columna, valor):
        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:
            matriz.valores[fila][columna] = valor
            return True
        return False

    def consultar_valor(self, matriz, fila, columna):
        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:
            return matriz.valores[fila][columna]
        return None
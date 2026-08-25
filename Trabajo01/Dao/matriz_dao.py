# ==========================================================
# IMPORTACIÓN DE LA INTERFAZ
# Se importa la interfaz que contiene las operaciones que
# debe implementar el DAO de la matriz.
# ==========================================================

from Dao.interfaz_matriz import InterfazMatriz

# ==========================================================
# CLASE MATRIZ DAO
# Contiene las operaciones encargadas de modificar y
# consultar los datos almacenados en la matriz.
# ==========================================================

class MatrizDAO(InterfazMatriz):

    # ======================================================
    # INSERTAR VALOR
    # Inserta un número entero o decimal en la posición
    # indicada por la fila y columna.
    # ======================================================
    def insertar_valor(self, matriz, fila, columna, valor):
        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:
            matriz.valores[fila][columna] = valor
            return True
        return False

    # ======================================================
    # CONSULTAR VALOR
    # Obtiene el valor almacenado en una posición específica
    # de la matriz después de comprobar que el índice sea
    # válido.
    # ======================================================

    def consultar_valor(self, matriz, fila, columna):
        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:
            return matriz.valores[fila][columna]
        return None

    # ======================================================
    # INTERCAMBIAR FILAS
    # Intercambia dos filas completas de la matriz.
    # Esta operación corresponde a una de las operaciones
    # elementales de matrices.
    # ======================================================
    def intercambiar_filas(self, matriz, fila1, fila2):
        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:
            matriz.valores[fila1], matriz.valores[fila2] = (
                matriz.valores[fila2],
                matriz.valores[fila1]
            )
            return True
        return False

    # ======================================================
    # SUMAR FILAS
    # Suma los elementos de la primera fila con los
    # elementos correspondientes de la segunda fila.
    # Operación:
    # F2 = F2 + F1
    # ======================================================

    def sumar_filas(self, matriz, fila1, fila2):
        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:
            for j in range(matriz.columnas):
                matriz.valores[fila2][j] += matriz.valores[fila1][j]
            return True
        return False

    # ======================================================
    # ESCALAR FILA
    # Multiplica cada elemento de una fila por el valor
    # escalar proporcionado por el usuario.
    # Operación:
    # F = kF
    # ======================================================

    def escalar_fila(self, matriz, fila, escalar):
        if 0 <= fila < matriz.filas:
            for j in range(matriz.columnas):
                matriz.valores[fila][j] *= escalar
            return True
        return False

    # ======================================================
    # SUMAR FILA ESCALADA
    # Multiplica una fila por un escalar y suma el resultado
    # a otra fila.
    # Operación:
    # F2 = F2 + kF1
    # ======================================================
    def sumar_fila_escalada(
        self,
        matriz,
        fila1,
        fila2,
        escalar
    ):
        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:
            for j in range(matriz.columnas):
                matriz.valores[fila2][j] += (
                    escalar * matriz.valores[fila1][j]
                )
            return True
        return False
from Dao.interfaz_matriz import InterfazMatriz

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

    def intercambiar_filas(self, matriz, fila1, fila2):

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            matriz.valores[fila1], matriz.valores[fila2] = (
                matriz.valores[fila2],
                matriz.valores[fila1]
            )

            return True

        return False

    def sumar_filas(self, matriz, fila1, fila2):

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            matriz.valores[fila2] = [
                matriz.valores[fila2][j] + matriz.valores[fila1][j]
                for j in range(matriz.columnas)
            ]

            return True

        return False

    def escalar_fila(self, matriz, fila, escalar):

        if 0 <= fila < matriz.filas:

            matriz.valores[fila] = [
                valor * escalar
                for valor in matriz.valores[fila]
            ]

            return True

        return False

    def sumar_fila_escalada(
        self,
        matriz,
        fila1,
        fila2,
        escalar
    ):

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            matriz.valores[fila2] = [
                matriz.valores[fila2][j]
                + escalar * matriz.valores[fila1][j]
                for j in range(matriz.columnas)
            ]

            return True

        return False
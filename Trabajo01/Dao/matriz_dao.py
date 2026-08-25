from Dao.interfaz_matriz import InterfazMatriz

class MatrizDAO(InterfazMatriz):

    def insertar_valor(self, matriz, fila, columna, valor):
        """
        Inserta un valor en una posición determinada.
        """

        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:

            matriz.valores[fila][columna] = valor

            return True

        return False

    def consultar_valor(self, matriz, fila, columna):
        """
        Consulta el valor de una posición determinada.
        """

        if 0 <= fila < matriz.filas and 0 <= columna < matriz.columnas:

            return matriz.valores[fila][columna]

        return None

    def intercambiar_filas(self, matriz, fila1, fila2):
        """
        Intercambia dos filas de la matriz.
        """

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            matriz.valores[fila1], matriz.valores[fila2] = (
                matriz.valores[fila2],
                matriz.valores[fila1]
            )

            return True

        return False

    def sumar_filas(self, matriz, fila1, fila2):
        """
        Suma la primera fila a la segunda:

        F2 = F2 + F1
        """

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            for j in range(matriz.columnas):

                matriz.valores[fila2][j] += matriz.valores[fila1][j]

            return True

        return False

    def escalar_fila(self, matriz, fila, escalar):
        """
        Multiplica todos los elementos de una fila
        por un escalar.
        """

        if 0 <= fila < matriz.filas:

            for j in range(matriz.columnas):

                matriz.valores[fila][j] *= escalar

            return True

        return False

    def sumar_fila_escalada(
        self,
        matriz,
        fila1,
        fila2,
        escalar
    ):
        """
        Realiza:

        F2 = F2 + escalar * F1
        """

        if 0 <= fila1 < matriz.filas and 0 <= fila2 < matriz.filas:

            for j in range(matriz.columnas):

                matriz.valores[fila2][j] += (
                    escalar * matriz.valores[fila1][j]
                )

            return True

        return False
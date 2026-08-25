class Matriz:

    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.valores = []

    def definir_tamano(self, filas, columnas):
        """
        Define el número de filas y columnas
        y crea una matriz vacía.
        """

        self.filas = filas
        self.columnas = columnas

        self.valores = []

        for i in range(filas):
            fila = []

            for j in range(columnas):
                fila.append(None)

            self.valores.append(fila)

    def esta_completa(self):
        """
        Comprueba si todos los espacios de la matriz
        contienen un valor.
        """

        if self.filas == 0 or self.columnas == 0:
            return False

        for fila in self.valores:

            for valor in fila:

                if valor is None:
                    return False

        return True

    def mostrar(self):
        """
        Muestra todos los valores de la matriz.
        """

        for fila in self.valores:
            print(fila)
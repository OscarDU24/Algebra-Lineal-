# ==========================================================
# SERVICIO DE ELIMINACIÓN
# Contiene el algoritmo encargado de transformar la matriz
# aumentada mediante operaciones elementales de filas para
# resolver el sistema de ecuaciones lineales.
# ==========================================================

class Eliminacion:
    def __init__(self, matriz):
        self.matriz = matriz

    # ======================================================
    # MOSTRAR PASO
    # Muestra la matriz después de una operación realizada
    # durante el proceso de eliminación.
    # ======================================================
    def mostrar_paso(self, mensaje):
        print(f"\n{mensaje}")
        self.matriz.mostrar()

    # ======================================================
    # ELIMINACIÓN POR FILAS
    # Utiliza cada pivote para convertir en cero los valores
    # que se encuentran debajo de él.
    # ======================================================
    def ejecutar(self):
        filas = self.matriz.filas
        columnas = self.matriz.columnas
        columna = 0
        pivotes = 0

        while pivotes < filas and columna < columnas - 1:
            fila_pivote = pivotes
            # --------------------------------------------------
            # BÚSQUEDA DEL PIVOTE
            # Busca una fila cuyo valor en la columna actual
            # sea diferente de cero.
            # --------------------------------------------------
            while fila_pivote < filas and self.matriz.valores[fila_pivote][columna] == 0:
                fila_pivote += 1
            if fila_pivote == filas:
                columna += 1
                continue

            # --------------------------------------------------
            # INTERCAMBIO DE FILAS
            # Si el pivote se encuentra en otra fila, se
            # intercambia con la fila actual.
            # --------------------------------------------------
            if fila_pivote != pivotes:
                self.matriz.valores[pivotes], self.matriz.valores[fila_pivote] = (
                    self.matriz.valores[fila_pivote],
                    self.matriz.valores[pivotes]
                )
                self.mostrar_paso(
                    f"Intercambio de filas {pivotes + 1} y {fila_pivote + 1}:"
                )

            # --------------------------------------------------
            # ELIMINACIÓN
            # Utiliza el pivote actual para convertir en cero
            # los elementos que se encuentran debajo.
            # --------------------------------------------------
            for i in range(pivotes + 1, filas):
                if self.matriz.valores[i][columna] != 0:
                    factor = (
                        self.matriz.valores[i][columna] /
                        self.matriz.valores[pivotes][columna]
                    )
                    for j in range(columna, columnas):
                        self.matriz.valores[i][j] -= (
                            factor * self.matriz.valores[pivotes][j]
                        )
                    self.mostrar_paso(
                        f"Eliminación de la fila {i + 1}:"
                    )
            pivotes += 1
            columna += 1
        return self.clasificar()

    # ======================================================
    # CLASIFICAR SISTEMA
    # Analiza las filas de la matriz resultante para determinar
    # si el sistema tiene solución única, infinitas soluciones
    # o ninguna solución.
    # ======================================================
    def clasificar(self):
        filas = self.matriz.filas
        variables = self.matriz.columnas - 1
        rango = 0
        for i in range(filas):
            tiene_coeficiente = False
            for j in range(variables):
                if self.matriz.valores[i][j] != 0:
                    tiene_coeficiente = True
                    break
            if not tiene_coeficiente and self.matriz.valores[i][variables] != 0:
                return "inconsistente"
            if tiene_coeficiente:
                rango += 1
        if rango == variables:
            return "determinado"
        return "indeterminado"

    # ======================================================
    # SUSTITUCIÓN HACIA ATRÁS
    # Obtiene los valores de las variables cuando el sistema
    # es consistente determinado.
    # ======================================================
    def obtener_solucion(self):
        variables = self.matriz.columnas - 1
        solucion = [0] * variables
        for i in range(variables - 1, -1, -1):
            suma = self.matriz.valores[i][variables]
            for j in range(i + 1, variables):
                suma -= self.matriz.valores[i][j] * solucion[j]
            solucion[i] = suma / self.matriz.valores[i][i]
        return solucion

    # ======================================================
    # VERIFICAR SOLUCIÓN
    # Sustituye las variables obtenidas en la matriz original
    # para comprobar que satisfacen las ecuaciones.
    # ======================================================
    def verificar(self, matriz_original, solucion):
        variables = len(solucion)
        for i in range(matriz_original.filas):
            resultado = 0
            for j in range(variables):
                resultado += (
                    matriz_original.valores[i][j] * solucion[j]
                )
            independiente = matriz_original.valores[i][variables]
            if abs(resultado - independiente) > 0.000001:
                return False
        return True
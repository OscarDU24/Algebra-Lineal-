# ==========================================================
# IMPORTACIÓN DE LIBRERÍA ESTÁNDAR
# ABC y abstractmethod permiten definir una interfaz que
# establece los métodos que deberá implementar el DAO.
# ==========================================================

from abc import ABC, abstractmethod


# ==========================================================
# INTERFAZ DE LA MATRIZ
# Define las operaciones que debe implementar la clase
# encargada de manipular los datos de la matriz.
# ==========================================================

class InterfazMatriz(ABC):

    # ======================================================
    # INSERTAR VALOR
    # Define el método encargado de insertar un valor en
    # una posición específica de la matriz.
    # ======================================================

    @abstractmethod
    def insertar_valor(self, matriz, fila, columna, valor):
        pass

    # ======================================================
    # CONSULTAR VALOR
    # Define el método encargado de obtener el valor ubicado
    # en una posición específica de la matriz.
    # ======================================================

    @abstractmethod
    def consultar_valor(self, matriz, fila, columna):
        pass

    # ======================================================
    # INTERCAMBIAR FILAS
    # Define el método utilizado para intercambiar dos filas.
    # ======================================================

    @abstractmethod
    def intercambiar_filas(self, matriz, fila1, fila2):
        pass

    # ======================================================
    # SUMAR FILAS
    # Define el método utilizado para sumar una fila con
    # otra fila de la matriz.
    # ======================================================

    @abstractmethod
    def sumar_filas(self, matriz, fila1, fila2):
        pass

    # ======================================================
    # ESCALAR FILA
    # Define el método utilizado para multiplicar los
    # elementos de una fila por un valor escalar.
    # ======================================================

    @abstractmethod
    def escalar_fila(self, matriz, fila, escalar):
        pass

    # ======================================================
    # SUMAR FILA ESCALADA
    # Define el método utilizado para sumar a una fila otra
    # fila multiplicada previamente por un escalar.
    # ======================================================

    @abstractmethod
    def sumar_fila_escalada(
        self,
        matriz,
        fila1,
        fila2,
        escalar
    ):
        pass
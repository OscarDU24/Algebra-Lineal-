from abc import ABC, abstractmethod

class InterfazMatriz(ABC):

    @abstractmethod
    def insertar_valor(self, matriz, fila, columna, valor):
        pass

    @abstractmethod
    def consultar_valor(self, matriz, fila, columna):
        pass

    @abstractmethod
    def intercambiar_filas(self, matriz, fila1, fila2):
        pass

    @abstractmethod
    def sumar_filas(self, matriz, fila1, fila2):
        pass

    @abstractmethod
    def escalar_fila(self, matriz, fila, escalar):
        pass

    @abstractmethod
    def sumar_fila_escalada(self, matriz, fila1, fila2, escalar):
        pass
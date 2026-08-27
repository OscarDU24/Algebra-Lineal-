# ==========================================================
# IMPORTACIÓN DE LA LIBRERÍA ESTÁNDAR
# ABC permite crear una clase abstracta que establece los
# métodos que deberá implementar el DAO.
# ==========================================================

from abc import ABC, abstractmethod

# ==========================================================
# INTERFAZ DE LA MATRIZ
# Define las operaciones básicas para insertar y consultar
# información de la matriz.
# ==========================================================

class InterfazMatriz(ABC):
    @abstractmethod
    def insertar_valor(self, matriz, fila, columna, valor):
        pass

    @abstractmethod
    def consultar_valor(self, matriz, fila, columna):
        pass
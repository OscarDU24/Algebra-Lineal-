"""Reglas comunes para distinguir cálculos exactos de aproximaciones.

Una matriz se procesa en modo exacto cuando contiene al menos un ``Fraction``
y ningún ``float``. En ese modo todos los valores se convierten a ``Fraction``
y un número es cero solo si es exactamente cero. Con datos ``float`` se
mantiene la tolerancia absoluta histórica del módulo.
"""

from fractions import Fraction


def es_matriz_exacta(matriz):
    """Indica si la matriz debe resolverse con aritmética racional exacta."""
    hay_fraccion = False
    for fila in matriz:
        for valor in fila:
            if isinstance(valor, float):
                return False
            if isinstance(valor, Fraction):
                hay_fraccion = True
    return hay_fraccion


def matriz_a_fracciones(matriz):
    """Copia la matriz convirtiendo enteros y fracciones a ``Fraction``."""
    return [[Fraction(valor) for valor in fila] for fila in matriz]


def es_cero(valor, exacto, tolerancia):
    """Compara con cero de forma exacta o con tolerancia según el modo."""
    if exacto:
        return valor == 0
    return abs(valor) < tolerancia


def es_uno(valor, exacto, tolerancia):
    """Compara con uno de forma exacta o con tolerancia según el modo."""
    if exacto:
        return valor == 1
    return abs(valor - 1) <= tolerancia

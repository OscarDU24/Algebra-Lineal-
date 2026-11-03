"""Compara inversión exacta y de punto flotante mediante Gauss-Jordan."""

from fractions import Fraction

import numpy as np

from core.sistemas.operaciones_sistemas import gauss_jordan


def parsear_matriz(texto):
    """Convierte filas separadas por salto de línea y celdas por espacios."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Ingrese una matriz cuadrada no vacía.")
    try:
        matriz = [
            [Fraction(valor) for valor in fila.replace(",", " ").split()]
            for fila in texto.strip().splitlines()
        ]
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("La matriz contiene una entrada numérica inválida.") from error
    orden = len(matriz)
    if orden == 0 or any(len(fila) != orden for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y tener filas completas.")
    return matriz


def matriz_hilbert(orden=5):
    if isinstance(orden, bool) or not isinstance(orden, int) or orden <= 0:
        raise ValueError("El orden de Hilbert debe ser un entero positivo.")
    return [
        [Fraction(1, fila + columna + 1) for columna in range(orden)]
        for fila in range(orden)
    ]


def comparar_inversas(matriz):
    """Compara A⁻¹ exacta, Gauss-Jordan float y NumPy, además del residuo."""
    exacta = _validar_matriz(matriz)
    orden = len(exacta)
    identidad_exacta = [
        [Fraction(int(fila == columna)) for columna in range(orden)]
        for fila in range(orden)
    ]
    aumentada_exacta = [
        fila[:] + identidad_exacta[indice][:]
        for indice, fila in enumerate(exacta)
    ]
    reducida_exacta, _ = gauss_jordan(aumentada_exacta)
    izquierda_exacta = [fila[:orden] for fila in reducida_exacta]
    if izquierda_exacta != identidad_exacta:
        raise ValueError("La matriz es singular y no posee inversa.")
    inversa_exacta = [fila[orden:] for fila in reducida_exacta]

    matriz_float = np.array(
        [[float(valor) for valor in fila] for fila in exacta],
        dtype=np.float64,
    )
    aumentada_float = [
        [float(valor) for valor in exacta[fila_indice]]
        + [float(fila_indice == columna) for columna in range(orden)]
        for fila_indice in range(orden)
    ]
    reducida_float, pivotes_float = gauss_jordan(aumentada_float)
    if pivotes_float < orden:
        raise ValueError("Gauss-Jordan en punto flotante detectó una matriz singular.")
    inversa_float = np.array(
        [fila[orden:] for fila in reducida_float],
        dtype=np.float64,
    )
    try:
        inversa_numpy = np.linalg.inv(matriz_float)
        condicion = float(np.linalg.cond(matriz_float))
    except np.linalg.LinAlgError as error:
        raise ValueError(
            "NumPy no pudo invertir la matriz; es singular o numéricamente singular: "
            f"{error}"
        ) from error
    if not np.all(np.isfinite(inversa_float)) or not np.all(np.isfinite(inversa_numpy)):
        raise ArithmeticError("La inversión produjo valores no finitos.")

    inversa_exacta_float = np.array(
        [[float(valor) for valor in fila] for fila in inversa_exacta],
        dtype=np.float64,
    )
    escala = float(np.max(np.abs(inversa_exacta_float)))
    if not np.isfinite(escala) or escala == 0:
        raise ArithmeticError(
            "La inversa exacta excede el rango representable en punto flotante."
        )
    error_gj_absoluto = float(
        np.max(np.abs(inversa_exacta_float - inversa_float))
    )
    error_numpy_absoluto = float(
        np.max(np.abs(inversa_exacta_float - inversa_numpy))
    )
    residual_gj = _residuo_maximo(matriz_float, inversa_float)
    residual_numpy = _residuo_maximo(matriz_float, inversa_numpy)
    return {
        "matriz": exacta,
        "inversa_exacta": inversa_exacta,
        "inversa_float": inversa_float.tolist(),
        "inversa_numpy": inversa_numpy.tolist(),
        "error_gj_absoluto": error_gj_absoluto,
        "error_gj_relativo": error_gj_absoluto / escala,
        "error_numpy_absoluto": error_numpy_absoluto,
        "error_numpy_relativo": error_numpy_absoluto / escala,
        "residuo_gj": residual_gj,
        "residuo_numpy": residual_numpy,
        "condicion": condicion,
    }


def matriz_a_texto(matriz, formato="fracciones"):
    if formato == "fracciones":
        return "\n".join(
            "[ " + "  ".join(_formatear_fraccion(valor) for valor in fila) + " ]"
            for fila in matriz
        )
    return "\n".join(
        "[ " + "  ".join(f"{float(valor):.8g}" for valor in fila) + " ]"
        for fila in matriz
    )


def _validar_matriz(matriz):
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError("La matriz debe ser cuadrada y no vacía.")
    orden = len(matriz)
    if any(not isinstance(fila, (list, tuple)) or len(fila) != orden for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y tener filas completas.")
    try:
        return [
            [
                valor if isinstance(valor, Fraction) else Fraction(str(valor))
                for valor in fila
            ]
            for fila in matriz
        ]
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError("La matriz contiene valores no numéricos.") from error


def _formatear_fraccion(valor):
    valor = valor if isinstance(valor, Fraction) else Fraction(valor)
    return str(valor.numerator) if valor.denominator == 1 else str(valor)


def _residuo_maximo(matriz, inversa):
    identidad_residuo = matriz @ inversa - np.eye(len(matriz), dtype=np.float64)
    return float(np.max(np.abs(identidad_residuo)))

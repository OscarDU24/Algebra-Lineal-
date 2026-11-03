"""Método de bisección con evaluación AST segura y contraste SciPy."""

import ast

import numpy as np
from scipy.optimize import bisect as scipy_bisect

from core.limites.operaciones_limites import _crear_evaluador

COLUMNAS_TABLA = (
    "Iteración",
    "xl",
    "xu",
    "xr",
    "f(xl)",
    "f(xu)",
    "f(xr)",
    "Ea (%)",
)


def _convertir_finito(valor, nombre):
    if isinstance(valor, bool):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    try:
        resultado = float(valor)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{nombre} debe ser un número real finito.") from error
    if not np.isfinite(resultado):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    return resultado


def _crear_funcion(funcion):
    if not isinstance(funcion, str) or not funcion.strip():
        raise ValueError("Ingrese una función válida en términos de x.")
    if len(funcion) > 300:
        raise ValueError("La función excede el límite de 300 caracteres.")
    try:
        arbol = ast.parse(funcion.replace("^", "**"), mode="eval")
        nodos = list(ast.walk(arbol))
        if len(nodos) > 100:
            raise ValueError("La función es demasiado compleja.")
        for nodo in nodos:
            if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Pow) and not (
                isinstance(nodo.right, ast.Constant)
                and isinstance(nodo.right.value, (int, float))
                and not isinstance(nodo.right.value, bool)
                and abs(nodo.right.value) <= 1000
            ):
                raise ValueError(
                    "Los exponentes deben ser constantes con valor absoluto ≤ 1000."
                )
        evaluador = _crear_evaluador(funcion)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError(
            "La función contiene sintaxis u operaciones no permitidas."
        ) from error

    def evaluar(x):
        try:
            resultado = evaluador(float(x))
            if isinstance(resultado, complex):
                raise ValueError("La función produjo un resultado complejo.")
            resultado = float(resultado)
        except (ArithmeticError, TypeError, ValueError, OverflowError) as error:
            raise ValueError(f"No se pudo evaluar f({x:g}): {error}") from error
        if not np.isfinite(resultado):
            raise ValueError(f"f({x:g}) produjo un resultado no finito.")
        return resultado

    return evaluar


def _iteraciones_teoricas(xl, xu, tolerancia):
    ancho = xu - xl
    if ancho <= tolerancia:
        return 0
    return max(0, int(np.ceil(np.log2(ancho) - np.log2(tolerancia))))


def _error_aproximado_porcentual(actual, anterior):
    if actual == 0:
        return 0.0 if anterior == 0 else float("inf")
    return abs((actual - anterior) / actual) * 100


def resolver_biseccion(funcion, a, b, tolerancia):
    """Calcula una raíz y retorna tabla estructurada y contraste con SciPy."""
    xl = _convertir_finito(a, "El extremo a")
    xu = _convertir_finito(b, "El extremo b")
    tol = _convertir_finito(tolerancia, "La tolerancia")
    if tol <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")
    if xl >= xu:
        raise ValueError("El intervalo debe cumplir a < b.")

    evaluar = _crear_funcion(funcion)
    f_xl = evaluar(xl)
    f_xu = evaluar(xu)
    if f_xl == 0:
        return _resultado_extremo(xl, f_xl, funcion, xl, xu, tol)
    if f_xu == 0:
        return _resultado_extremo(xu, f_xu, funcion, xl, xu, tol)
    if np.signbit(f_xl) == np.signbit(f_xu):
        raise ValueError(
            "El intervalo no presenta cambio de signo: f(a) y f(b) "
            "deben tener signos opuestos."
        )

    teoricas = _iteraciones_teoricas(xl, xu, tol)
    max_iteraciones = max(1, teoricas + 2)
    tabla = []
    xr_anterior = None
    xr = (xl + xu) / 2
    f_xr = evaluar(xr)
    ea = None
    criterio = "ancho del intervalo"

    for iteracion in range(1, max_iteraciones + 1):
        xr = xl + (xu - xl) / 2
        if xr == xl or xr == xu:
            raise ArithmeticError(
                "La precisión de punto flotante impide seguir reduciendo el intervalo."
            )
        f_xr = evaluar(xr)
        ea = (
            _error_aproximado_porcentual(xr, xr_anterior)
            if xr_anterior is not None
            else None
        )
        tabla.append([iteracion, xl, xu, xr, f_xl, f_xu, f_xr, ea])

        if f_xr == 0:
            criterio = "raíz exacta"
            break
        if np.signbit(f_xl) != np.signbit(f_xr):
            xu, f_xu = xr, f_xr
        else:
            xl, f_xl = xr, f_xr

        if xu - xl < tol:
            criterio = "ancho del intervalo"
            break
        if ea is not None and ea < tol:
            criterio = "error aproximado porcentual"
            break
        xr_anterior = xr
    else:
        raise ArithmeticError(
            f"No se alcanzó la tolerancia tras {max_iteraciones} iteraciones."
        )

    try:
        raiz_scipy = float(
            scipy_bisect(
                evaluar,
                _convertir_finito(a, "El extremo a"),
                _convertir_finito(b, "El extremo b"),
                xtol=tol,
                maxiter=max(100, max_iteraciones + 5),
            )
        )
    except (RuntimeError, ValueError, ArithmeticError) as error:
        raise ArithmeticError(
            f"Bisección propia convergió, pero SciPy no pudo completar el contraste: {error}"
        ) from error

    return {
        "raiz": xr,
        "f_raiz": f_xr,
        "raiz_scipy": raiz_scipy,
        "diferencia_absoluta": abs(xr - raiz_scipy),
        "iteraciones": len(tabla),
        "iteraciones_teoricas": teoricas,
        "criterio_paro": criterio,
        "columnas": COLUMNAS_TABLA,
        "tabla": tabla,
    }


def _resultado_extremo(raiz, valor_funcion, funcion, xl, xu, tolerancia):
    evaluar = _crear_funcion(funcion)
    try:
        raiz_scipy = float(
            scipy_bisect(
                evaluar,
                xl,
                xu,
                xtol=tolerancia,
                maxiter=100,
            )
        )
    except (RuntimeError, ValueError, ArithmeticError) as error:
        raise ArithmeticError(
            f"No se pudo contrastar con SciPy la raíz del extremo: {error}"
        ) from error
    return {
        "raiz": raiz,
        "f_raiz": valor_funcion,
        "raiz_scipy": raiz_scipy,
        "diferencia_absoluta": abs(raiz - raiz_scipy),
        "iteraciones": 0,
        "iteraciones_teoricas": _iteraciones_teoricas(xl, xu, tolerancia),
        "criterio_paro": "raíz en un extremo",
        "columnas": COLUMNAS_TABLA,
        "tabla": [],
    }


def formatear_tabla(resultado):
    """Renderiza la tabla de iteraciones con ancho monoespaciado."""
    columnas = resultado["columnas"]
    filas = resultado["tabla"]
    anchos = [
        max(
            [len(columna)]
            + [len(_formatear_celda(fila[indice])) for fila in filas]
        )
        for indice, columna in enumerate(columnas)
    ]
    encabezado = " | ".join(
        columna.ljust(anchos[indice]) for indice, columna in enumerate(columnas)
    )
    separador = "-+-".join("-" * ancho for ancho in anchos)
    cuerpo = [
        " | ".join(
            _formatear_celda(valor).ljust(anchos[indice])
            for indice, valor in enumerate(fila)
        )
        for fila in filas
    ]
    return "\n".join([encabezado, separador, *cuerpo])


def _formatear_celda(valor):
    if valor is None:
        return "—"
    if isinstance(valor, float) and not np.isfinite(valor):
        return "∞"
    if isinstance(valor, int):
        return str(valor)
    return f"{valor:.10g}"

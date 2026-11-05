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
        nombres_permitidos = {
            "x", "pi", "e", "sin", "sen", "cos", "tan", "tg",
            "sqrt", "raiz", "exp", "log", "ln", "abs",
        }
        nombres_funcion = {
            id(nodo.func)
            for nodo in nodos
            if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
        }
        operaciones_binarias = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
        tipos_permitidos = (
            ast.Expression,
            ast.Constant,
            ast.Name,
            ast.Load,
            ast.UnaryOp,
            ast.UAdd,
            ast.USub,
            ast.BinOp,
            *operaciones_binarias,
            ast.Call,
        )
        for nodo in nodos:
            if not isinstance(nodo, tipos_permitidos):
                raise ValueError("La función contiene una construcción no permitida.")
            if isinstance(nodo, ast.Constant) and (
                not isinstance(nodo.value, (int, float))
                or isinstance(nodo.value, bool)
            ):
                raise ValueError("La función solo admite constantes numéricas.")
            if isinstance(nodo, ast.Name) and (
                nodo.id not in nombres_permitidos
                or (
                    nodo.id not in {"x", "pi", "e"}
                    and id(nodo) not in nombres_funcion
                )
            ):
                raise ValueError(f"Nombre no permitido en la función: {nodo.id}.")
            if isinstance(nodo, ast.Call) and (
                not isinstance(nodo.func, ast.Name)
                or nodo.func.id not in nombres_permitidos
                or nodo.func.id in {"x", "pi", "e"}
                or len(nodo.args) != 1
                or nodo.keywords
            ):
                raise ValueError("La función contiene una llamada no permitida.")
            if isinstance(nodo, ast.BinOp) and not isinstance(
                nodo.op, operaciones_binarias
            ):
                raise ValueError("La función contiene un operador no permitido.")
            if isinstance(nodo, ast.UnaryOp) and not isinstance(
                nodo.op, (ast.UAdd, ast.USub)
            ):
                raise ValueError("La función contiene un operador no permitido.")
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


def muestrear_funcion(funcion, x_min, x_max, muestras=400):
    """Devuelve coordenadas para graficar la función en un rango finito."""
    minimo = _convertir_finito(x_min, "El límite inferior")
    maximo = _convertir_finito(x_max, "El límite superior")
    if minimo >= maximo:
        raise ValueError("El rango de la gráfica debe cumplir x_min < x_max.")
    if not np.isfinite(maximo - minimo):
        raise ValueError("El ancho del rango de la gráfica debe ser finito.")
    if isinstance(muestras, bool) or not isinstance(muestras, int):
        raise ValueError("La cantidad de muestras debe ser un entero.")
    if not 3 <= muestras <= 5000:
        raise ValueError("La cantidad de muestras debe estar entre 3 y 5000.")

    evaluar = _crear_funcion(funcion)
    puntos = np.linspace(minimo, maximo, muestras)
    valores = []
    for punto in puntos:
        try:
            valores.append(evaluar(float(punto)))
        except (ValueError, ArithmeticError, OverflowError):
            valores.append(None)

    return {
        "x": puntos.tolist(),
        "y": [np.nan if valor is None else valor for valor in valores],
        "muestras": muestras,
        "rango": (minimo, maximo),
    }


def analizar_intervalos(funcion, x_min, x_max, muestras=400):
    """Muestrea f(x) y devuelve tramos candidatos con cambio de signo."""
    datos = muestrear_funcion(funcion, x_min, x_max, muestras)
    puntos = datos["x"]
    valores = [None if np.isnan(valor) else valor for valor in datos["y"]]
    minimo, maximo = datos["rango"]
    muestras = datos["muestras"]

    candidatos = []
    raices_muestreadas = {
        indice for indice, valor in enumerate(valores)
        if valor == 0
    }

    for indice in sorted(raices_muestreadas):
        vecino = indice - 1
        if vecino < 0 or valores[vecino] is None or valores[vecino] == 0:
            vecino = indice + 1
        if vecino >= muestras or valores[vecino] is None or valores[vecino] == 0:
            continue
        primero, segundo = sorted((indice, vecino))
        candidatos.append({
            "a": float(puntos[primero]),
            "b": float(puntos[segundo]),
            "fa": valores[primero],
            "fb": valores[segundo],
            "raiz_muestreada": float(puntos[indice]),
        })

    for indice in range(muestras - 1):
        valor_izquierdo = valores[indice]
        valor_derecho = valores[indice + 1]
        if (
            valor_izquierdo is None
            or valor_derecho is None
            or valor_izquierdo == 0
            or valor_derecho == 0
        ):
            continue
        if np.signbit(valor_izquierdo) != np.signbit(valor_derecho):
            candidatos.append({
                "a": float(puntos[indice]),
                "b": float(puntos[indice + 1]),
                "fa": valor_izquierdo,
                "fb": valor_derecho,
                "raiz_muestreada": None,
            })

    candidatos.sort(key=lambda intervalo: intervalo["a"])
    valores_finitos = [valor for valor in valores if valor is not None]
    if valores_finitos and all(valor == 0 for valor in valores_finitos):
        raise ValueError(
            "La función es cero en todo el rango muestreado; no se detecta una raíz aislada."
        )

    return {**datos, "intervalos": candidatos}


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
    if not np.isfinite(xu - xl):
        raise ValueError("El ancho del intervalo debe ser finito.")

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

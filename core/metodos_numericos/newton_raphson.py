"""Método de Newton-Raphson con derivada evaluada mediante AST seguro."""

from core.metodos_numericos.biseccion import _convertir_finito, _crear_funcion, _es_finito

COLUMNAS_TABLA = (
    "Iteración",
    "x_n",
    "f(x_n)",
    "f'(x_n)",
    "x_{n+1}",
    "|Δx|",
    "|f(x_{n+1})|",
)


def _derivada_numerica(funcion, x):
    evaluar = _crear_funcion(funcion)
    h = 1e-8 * max(1.0, abs(float(x)))
    if h == 0:
        h = 1e-8
    return (evaluar(x + h) - evaluar(x - h)) / (2 * h)


def _derivada_evaluada(funcion, derivada, x):
    if derivada is None or not str(derivada).strip():
        return _derivada_numerica(funcion, x)
    evaluar_derivada = _crear_funcion(derivada)
    return evaluar_derivada(x)


def _convertir_max_iteraciones(valor):
    if isinstance(valor, bool):
        raise ValueError("El máximo de iteraciones debe ser un entero entre 1 y 100000.")
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor:
            raise ValueError("Ingrese el máximo de iteraciones (un número entero).")
        try:
            valor = int(valor)
        except ValueError as error:
            raise ValueError("El máximo de iteraciones debe ser un número entero.") from error
    elif not isinstance(valor, int):
        raise ValueError("El máximo de iteraciones debe ser un número entero.")
    if not 1 <= valor <= 100000:
        raise ValueError("El máximo de iteraciones debe ser un entero entre 1 y 100000.")
    return valor


def _resultado(*, raiz, convergio, estado, iteraciones, tolerancia, tabla):
    return {
        "raiz": raiz,
        "convergio": convergio,
        "estado": estado,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia,
        "criterio_paro": estado,
        "columnas": COLUMNAS_TABLA,
        "tabla": tabla,
    }


def resolver_newton_raphson(funcion, x_inicial, tolerancia, max_iteraciones, derivada=None):
    """Resuelve f(x)=0 con el método de Newton-Raphson."""
    evaluar = _crear_funcion(funcion)
    x_actual = _convertir_finito(x_inicial, "El valor inicial x0")
    tol = _convertir_finito(tolerancia, "La tolerancia")
    if tol <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")
    max_iteraciones = _convertir_max_iteraciones(max_iteraciones)

    f_x = evaluar(x_actual)
    if abs(f_x) <= tol:
        return _resultado(
            raiz=x_actual,
            convergio=True,
            estado="Raíz exacta en x0",
            iteraciones=0,
            tolerancia=tol,
            tabla=[],
        )

    tabla = []
    convergio = False
    estado = "Máximo de iteraciones alcanzado"
    x_anterior = x_actual

    for iteracion in range(1, max_iteraciones + 1):
        f_x = evaluar(x_actual)
        derivada_val = _derivada_evaluada(funcion, derivada, x_actual)
        if not _es_finito(derivada_val) or derivada_val == 0:
            raise ValueError(
                "La derivada es cero o no finita en x = "
                f"{x_actual:g}. Cambie el punto inicial o proporcione f'(x)."
            )

        x_siguiente = x_actual - (f_x / derivada_val)
        if not _es_finito(x_siguiente):
            raise ArithmeticError("La próxima iteración produce un valor no finito.")

        f_siguiente = evaluar(x_siguiente)
        delta_x = abs(x_siguiente - x_actual)
        residuo = abs(f_siguiente)
        tabla.append([
            iteracion,
            x_actual,
            f_x,
            derivada_val,
            x_siguiente,
            delta_x,
            residuo,
        ])

        if residuo <= tol:
            convergio = True
            estado = "Tolerancia por residuo alcanzada"
            x_actual = x_siguiente
            break
        if delta_x <= tol:
            convergio = True
            estado = "Tolerancia por cambio entre aproximaciones alcanzada"
            x_actual = x_siguiente
            break

        x_anterior = x_actual
        x_actual = x_siguiente

    return _resultado(
        raiz=x_actual,
        convergio=convergio,
        estado=estado,
        iteraciones=len(tabla),
        tolerancia=tol,
        tabla=tabla,
    )


def _formatear_celda(valor):
    if valor is None:
        return "—"
    if isinstance(valor, float):
        if not _es_finito(valor):
            return "∞" if valor > 0 else "-∞"
        return f"{valor:.10g}"
    return str(valor)


def formatear_tabla(resultado):
    """Formatea la tabla que registra cada iteración del método."""
    columnas = resultado["columnas"]
    filas = resultado["tabla"]
    anchos = [
        max([len(columna)] + [len(_formatear_celda(fila[indice])) for fila in filas])
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

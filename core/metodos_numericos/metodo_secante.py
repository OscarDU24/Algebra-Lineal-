"""Método de la secante con evaluación algebraica segura."""

from core.metodos_numericos.biseccion import (
    _convertir_finito,
    _crear_funcion,
    _es_finito,
)

COLUMNAS_TABLA = (
    "Iteración",
    "x_{n-1}",
    "x_n",
    "f(x_{n-1})",
    "f(x_n)",
    "x_{n+1}",
    "|Δx|",
    "|f(x_{n+1})|",
)


def _convertir_max_iteraciones(valor):
    if isinstance(valor, bool):
        raise ValueError(
            "El máximo de iteraciones debe ser un entero entre 1 y 100000."
        )
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor:
            raise ValueError("Ingrese el máximo de iteraciones (un número entero).")
        try:
            valor = int(valor)
        except ValueError as error:
            raise ValueError(
                "El máximo de iteraciones debe ser un número entero."
            ) from error
    elif not isinstance(valor, int):
        raise ValueError("El máximo de iteraciones debe ser un número entero.")
    if not 1 <= valor <= 100000:
        raise ValueError(
            "El máximo de iteraciones debe ser un entero entre 1 y 100000."
        )
    return valor


def _resultado(
    *,
    raiz,
    convergio,
    estado,
    iteraciones,
    tolerancia,
    tabla,
    procedimiento_secante,
):
    return {
        "raiz": raiz,
        "convergio": convergio,
        "estado": estado,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia,
        "criterio_paro": estado,
        "columnas": COLUMNAS_TABLA,
        "tabla": tabla,
        "procedimiento_secante": procedimiento_secante,
    }


def resolver_secante(funcion, x_anterior, x_actual, tolerancia, max_iteraciones):
    """Resuelve f(x)=0 con dos aproximaciones iniciales."""
    evaluar = _crear_funcion(funcion)
    x_anterior = _convertir_finito(x_anterior, "El valor inicial x0")
    x_actual = _convertir_finito(x_actual, "El valor inicial x1")
    tol = _convertir_finito(tolerancia, "La tolerancia")
    if tol <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")
    max_iteraciones = _convertir_max_iteraciones(max_iteraciones)

    f_anterior = evaluar(x_anterior)
    f_actual = evaluar(x_actual)
    if abs(f_anterior) <= tol:
        return _resultado(
            raiz=x_anterior,
            convergio=True,
            estado="Raíz aproximada en x0",
            iteraciones=0,
            tolerancia=tol,
            tabla=[],
            procedimiento_secante=[],
        )
    if abs(f_actual) <= tol:
        return _resultado(
            raiz=x_actual,
            convergio=True,
            estado="Raíz aproximada en x1",
            iteraciones=0,
            tolerancia=tol,
            tabla=[],
            procedimiento_secante=[],
        )

    tabla = []
    procedimiento_secante = []
    estado = "Máximo de iteraciones alcanzado"
    convergio = False

    for iteracion in range(1, max_iteraciones + 1):
        denominador = f_actual - f_anterior
        if not _es_finito(denominador) or denominador == 0:
            raise ValueError(
                "El denominador f(x_n) - f(x_{n-1}) es cero o no finito. "
                "Cambie los valores iniciales."
            )

        diferencia_x = x_actual - x_anterior
        numerador = f_actual * diferencia_x
        if not _es_finito(numerador):
            raise ArithmeticError(
                "El numerador de la secante produjo un valor no finito."
            )
        correccion = numerador / denominador
        x_siguiente = x_actual - correccion
        if not _es_finito(x_siguiente):
            raise ArithmeticError("La próxima iteración produce un valor no finito.")

        f_siguiente = evaluar(x_siguiente)
        delta_x = abs(x_siguiente - x_actual)
        residuo = abs(f_siguiente)
        tabla.append(
            [
                iteracion,
                x_anterior,
                x_actual,
                f_anterior,
                f_actual,
                x_siguiente,
                delta_x,
                residuo,
            ]
        )
        procedimiento_secante.append(
            {
                "x_anterior": x_anterior,
                "x_actual": x_actual,
                "f_anterior": f_anterior,
                "f_actual": f_actual,
                "diferencia_x": diferencia_x,
                "numerador": numerador,
                "denominador": denominador,
                "correccion": correccion,
                "x_siguiente": x_siguiente,
                "f_siguiente": f_siguiente,
                "delta_x": delta_x,
                "residuo": residuo,
            }
        )

        if residuo <= tol:
            convergio = True
            estado = "Tolerancia por residuo alcanzada"
            x_actual = x_siguiente
            break
        if x_siguiente == x_actual:
            estado = "Estancamiento: la aproximación dejó de cambiar"
            break
        if delta_x <= tol:
            convergio = True
            estado = "Tolerancia por cambio entre aproximaciones alcanzada"
            x_actual = x_siguiente
            break

        x_anterior, f_anterior = x_actual, f_actual
        x_actual, f_actual = x_siguiente, f_siguiente

    return _resultado(
        raiz=x_actual,
        convergio=convergio,
        estado=estado,
        iteraciones=len(tabla),
        tolerancia=tol,
        tabla=tabla,
        procedimiento_secante=procedimiento_secante,
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
    """Formatea la tabla de iteraciones en columnas monoespaciadas."""
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

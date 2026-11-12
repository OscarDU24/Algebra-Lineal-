from newton_raphson import COLUMNAS_TABLA, PASO_RELATIVO_DERIVADA, FORMULA_DERIVADA, _derivada_numerica, _convertir_max_iteraciones, _resultado, _formatear_celda, formatear_tabla


def resolver_secante(funcion, x_anterior, x_actual, tolerancia, max_iteraciones):
    """Resuelve f(x)=0 con el método de la secante."""
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
    convergio = False
    estado = "Máximo de iteraciones alcanzado"

    for iteracion in range(1, max_iteraciones + 1):
        denominador = f_actual - f_anterior

        if not _es_finito(denominador) or denominador == 0:
            raise ValueError(
                "El denominador es cero o no finito. "
                "Cambie los valores iniciales."
            )

        x_siguiente = x_actual - (
            f_actual * (x_actual - x_anterior) / denominador
        )

        if not _es_finito(x_siguiente):
            raise ArithmeticError(
                "La próxima iteración produce un valor no finito."
            )

        f_siguiente = evaluar(x_siguiente)

        delta_x = abs(x_siguiente - x_actual)
        residuo = abs(f_siguiente)

        tabla.append([
            iteracion,
            x_anterior,
            x_actual,
            f_anterior,
            f_actual,
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
        f_anterior = f_actual
        x_actual = x_siguiente
        f_actual = f_siguiente

    return _resultado(
        raiz=x_actual,
        convergio=convergio,
        estado=estado,
        iteraciones=len(tabla),
        tolerancia=tol,
        tabla=tabla,
        procedimiento_secante=procedimiento_secante,
    )

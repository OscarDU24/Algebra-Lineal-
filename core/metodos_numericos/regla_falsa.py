"""Método Regula Falsi con evaluación algebraica segura."""

from core.metodos_numericos.biseccion import (
    _convertir_finito,
    _crear_funcion,
    _es_finito,
)

COLUMNAS_TABLA = (
    "Iteración",
    "a",
    "b",
    "f(a)",
    "f(b)",
    "c",
    "f(c)",
    "Reemplazo",
    "Ea (%)",
)


def calcular_punto_c(a, b, fa, fb):
    """Calcula la intersección de la secante con el eje x de forma estable."""
    denominador = abs(fa) + abs(fb)
    if not _es_finito(denominador):
        if abs(fa) >= abs(fb):
            proporcion = 1 / (1 + abs(fb) / abs(fa))
        else:
            razon = abs(fa) / abs(fb)
            proporcion = razon / (1 + razon)
    else:
        if denominador == 0:
            raise ValueError(
                "No se puede calcular c porque f(a) y f(b) son ambos cero."
            )
        proporcion = abs(fa) / denominador

    c = a + (b - a) * proporcion
    if not _es_finito(c):
        raise ArithmeticError("El punto de falsa posición no es finito.")
    return float(c)


def calcular_error(c_actual, c_anterior):
    """Devuelve el error relativo aproximado en porcentaje."""
    if c_actual == 0:
        return 0.0 if c_anterior == 0 else float("inf")
    return abs((c_actual - c_anterior) / c_actual) * 100


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
    aproximacion,
    f_aproximacion,
    convergio,
    estado,
    iteraciones,
    tolerancia,
    tabla,
):
    return {
        "raiz": raiz,
        "aproximacion": aproximacion,
        "f_aproximacion": f_aproximacion,
        "convergio": convergio,
        "estado": estado,
        "iteraciones": iteraciones,
        "tolerancia_porcentual": tolerancia,
        "criterio_paro": "error relativo aproximado porcentual",
        "columnas": COLUMNAS_TABLA,
        "tabla": tabla,
    }


def resolver_regla_falsa(funcion, a, b, tolerancia, max_iteraciones):
    """Resuelve f(x)=0; la tolerancia se expresa en porcentaje de Ea."""
    extremo_a = _convertir_finito(a, "El extremo a")
    extremo_b = _convertir_finito(b, "El extremo b")
    tol = _convertir_finito(tolerancia, "La tolerancia porcentual")
    if tol <= 0:
        raise ValueError("La tolerancia porcentual debe ser mayor que cero.")
    if extremo_a >= extremo_b:
        raise ValueError("El intervalo debe cumplir a < b.")
    if not _es_finito(extremo_b - extremo_a):
        raise ValueError("El ancho del intervalo debe ser finito.")
    max_iteraciones = _convertir_max_iteraciones(max_iteraciones)

    evaluar = _crear_funcion(funcion)
    fa = evaluar(extremo_a)
    fb = evaluar(extremo_b)
    if fa == 0:
        return _resultado(
            raiz=extremo_a,
            aproximacion=extremo_a,
            f_aproximacion=fa,
            convergio=True,
            estado="Raíz exacta en a",
            iteraciones=0,
            tolerancia=tol,
            tabla=[],
        )
    if fb == 0:
        return _resultado(
            raiz=extremo_b,
            aproximacion=extremo_b,
            f_aproximacion=fb,
            convergio=True,
            estado="Raíz exacta en b",
            iteraciones=0,
            tolerancia=tol,
            tabla=[],
        )
    if (fa < 0) == (fb < 0):
        raise ValueError(
            "El intervalo no presenta cambio de signo: f(a) y f(b) "
            "deben tener signos opuestos."
        )

    tabla = []
    c_anterior = None
    c = None
    fc = None
    estado = "Máximo de iteraciones alcanzado"
    convergio = False

    for iteracion in range(1, max_iteraciones + 1):
        c = calcular_punto_c(extremo_a, extremo_b, fa, fb)
        if c <= extremo_a or c >= extremo_b:
            fc = fa if c <= extremo_a else fb
            tabla.append(
                [
                    iteracion,
                    extremo_a,
                    extremo_b,
                    fa,
                    fb,
                    c,
                    fc,
                    "Sin avance por precisión",
                    None,
                ]
            )
            estado = "Límite de precisión: el intervalo no puede avanzar"
            break

        fc = evaluar(c)
        error = (
            None
            if c_anterior is None
            else calcular_error(c, c_anterior)
        )
        if fc == 0:
            reemplazo = "Raíz exacta"
        elif (fa < 0) != (fc < 0):
            reemplazo = "b = c"
        else:
            reemplazo = "a = c"

        tabla.append(
            [
                iteracion,
                extremo_a,
                extremo_b,
                fa,
                fb,
                c,
                fc,
                reemplazo,
                error,
            ]
        )

        if fc == 0:
            convergio = True
            estado = "Raíz exacta encontrada"
            break

        if c_anterior is not None and c == c_anterior:
            estado = "Estancamiento: la aproximación dejó de cambiar"
            break
        if error is not None and error <= tol:
            convergio = True
            estado = "Tolerancia de error aproximado alcanzada"
            break

        if (fa < 0) != (fc < 0):
            extremo_b, fb = c, fc
        else:
            extremo_a, fa = c, fc
        c_anterior = c

    return _resultado(
        raiz=c if convergio else None,
        aproximacion=c,
        f_aproximacion=fc,
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
        if valor != valor:
            return "—"
        if valor in (float("inf"), float("-inf")):
            return "∞" if valor > 0 else "-∞"
        return f"{valor:.10g}"
    return str(valor)


def formatear_tabla(resultado):
    """Formatea las filas estructuradas para una consola monoespaciada."""
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
        columna.ljust(anchos[indice])
        for indice, columna in enumerate(columnas)
    )
    separador = "-+-".join("-" * ancho for ancho in anchos)
    contenido = [
        " | ".join(
            _formatear_celda(valor).ljust(anchos[indice])
            for indice, valor in enumerate(fila)
        )
        for fila in filas
    ]
    return "\n".join([encabezado, separador, *contenido])

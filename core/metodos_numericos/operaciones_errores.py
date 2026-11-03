"""Cálculo y demostración de errores numéricos."""

from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP, localcontext

import numpy as np

from core.metodos_numericos.biseccion import _crear_funcion, _convertir_finito


def calcular_errores(valor_aproximado, valor_exacto):
    aproximado = _convertir_finito(valor_aproximado, "El valor aproximado")
    exacto = _convertir_finito(valor_exacto, "El valor exacto")
    absoluto = abs(aproximado - exacto)
    if exacto == 0:
        relativo = 0.0 if absoluto == 0 else None
        porcentual = 0.0 if absoluto == 0 else None
    else:
        relativo = absoluto / abs(exacto)
        porcentual = relativo * 100
    return {
        "error_absoluto": absoluto,
        "error_relativo": relativo,
        "error_porcentual": porcentual,
    }


def propagar_error(funcion, x, delta_x):
    """Compara la aproximación diferencial con el cambio finito real."""
    evaluar = _crear_funcion(funcion)
    punto = _convertir_finito(x, "x")
    variacion = _convertir_finito(delta_x, "Δx")
    paso = np.cbrt(np.finfo(float).eps) * max(1.0, abs(punto))
    derivada = (evaluar(punto + paso) - evaluar(punto - paso)) / (2 * paso)
    cambio_aproximado = derivada * variacion
    cambio_exacto = evaluar(punto + variacion) - evaluar(punto)
    if not all(
        np.isfinite(valor)
        for valor in (derivada, cambio_aproximado, cambio_exacto)
    ):
        raise ValueError("La propagación produjo un valor no finito.")
    return {
        "derivada_aproximada": float(derivada),
        "delta_y_aproximado": float(cambio_aproximado),
        "delta_y_exacto": float(cambio_exacto),
        "error_absoluto_aproximacion": abs(cambio_aproximado - cambio_exacto),
    }


def simular_truncamiento_redondeo(valor, decimales):
    numero = _convertir_finito(valor, "El valor")
    if isinstance(decimales, bool) or not isinstance(decimales, int) or decimales < 0:
        raise ValueError("La cantidad de decimales debe ser un entero no negativo.")
    cuantizador = Decimal(1).scaleb(-decimales)
    valor_decimal = Decimal(str(numero))
    try:
        with localcontext() as contexto:
            contexto.prec = max(50, len(valor_decimal.as_tuple().digits) + decimales + 5)
            truncado = valor_decimal.quantize(cuantizador, rounding=ROUND_DOWN)
            redondeado = valor_decimal.quantize(cuantizador, rounding=ROUND_HALF_UP)
    except InvalidOperation as error:
        raise ValueError("No se pudo representar el número con esa precisión.") from error
    return {
        "original": numero,
        "decimales": decimales,
        "truncado": float(truncado),
        "redondeado": float(redondeado),
        "error_truncamiento": abs(numero - float(truncado)),
        "error_redondeo": abs(numero - float(redondeado)),
    }


def demostrar_punto_flotante():
    """Retorna valores reproducibles para una demostración IEEE-754."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        valor_overflow = np.float32(3.4e38) * np.float32(2.0)
        valor_underflow = np.float32(1e-30) * np.float32(1e-20)
    return {
        "suma_0_1_0_2": 0.1 + 0.2,
        "suma_0_1_0_2_igual_0_3": (0.1 + 0.2) == 0.3,
        "epsilon_float64": float(np.finfo(float).eps),
        "overflow_float32": float(valor_overflow),
        "overflow_es_infinito": bool(np.isinf(valor_overflow)),
        "underflow_float32": float(valor_underflow),
        "underflow_es_cero": bool(valor_underflow == 0),
        "menor_normal_float32": float(np.finfo(np.float32).tiny),
    }

"""Calculo numerico de limites usando unicamente Python estandar.

Las funciones elementales delegan en el modulo ``math`` de la biblioteca
estandar: realiza la reduccion de argumento en tiempo constante y ofrece
precision de doble en todo el rango de ``float``. Las series manuales
anteriores congelaban la interfaz con argumentos grandes (``sin(1e300)``) y
perdian exactitud en ``sqrt`` y ``exp``.
"""

import ast
import logging
import math

PI = math.pi
E = math.e
TOLERANCIA = 1e-7


def _valor_absoluto(valor):
    return valor if valor >= 0 else -valor


def _reducir_angulo(valor):
    """Lleva el angulo a [-pi, pi] en tiempo constante."""
    if not math.isfinite(valor):
        raise ValueError("Las funciones trigonometricas requieren un argumento finito.")
    return math.remainder(valor, 2 * PI)


def _seno(valor):
    if not math.isfinite(valor):
        raise ValueError("Las funciones trigonometricas requieren un argumento finito.")
    return math.sin(valor)


def _coseno(valor):
    if not math.isfinite(valor):
        raise ValueError("Las funciones trigonometricas requieren un argumento finito.")
    return math.cos(valor)


def _raiz_cuadrada(valor):
    if valor < 0:
        raise ValueError("La raíz cuadrada requiere un valor no negativo.")
    return math.sqrt(valor)


def _exponencial(valor):
    try:
        return math.exp(valor)
    except OverflowError:
        # Se conserva el comportamiento previo: el desbordamiento se informa
        # como valor infinito y cada evaluador decide como reportarlo.
        return math.inf


def _logaritmo(valor):
    if valor <= 0:
        raise ValueError("El logaritmo requiere un valor positivo.")
    return math.log(valor)


def _tangente(valor):
    coseno = _coseno(valor)
    if _valor_absoluto(coseno) < TOLERANCIA:
        raise ValueError("La tangente no está definida en este punto.")
    return _seno(valor) / coseno


def _reciproca_trigonometrica(nombre, denominador):
    if _valor_absoluto(denominador) < TOLERANCIA:
        raise ValueError(f"{nombre} no está definida en este punto.")
    return 1 / denominador


def _cosecante(valor):
    return _reciproca_trigonometrica("La cosecante", _seno(valor))


def _secante(valor):
    return _reciproca_trigonometrica("La secante", _coseno(valor))


def _cotangente(valor):
    return _reciproca_trigonometrica("La cotangente", _seno(valor)) * _coseno(valor)


FUNCIONES = {
    "sin": _seno,
    "sen": _seno,
    "cos": _coseno,
    "tan": _tangente,
    "tg": _tangente,
    "csc": _cosecante,
    "cosec": _cosecante,
    "cosecante": _cosecante,
    "sec": _secante,
    "secante": _secante,
    "cot": _cotangente,
    "cotg": _cotangente,
    "cotan": _cotangente,
    "cotangente": _cotangente,
    "sqrt": _raiz_cuadrada,
    "raiz": _raiz_cuadrada,
    "exp": _exponencial,
    "log": _logaritmo,
    "ln": _logaritmo,
    "abs": abs,
}


def _evaluar_arbol(arbol, valor_x):
    if isinstance(arbol, ast.Expression):
        return _evaluar_arbol(arbol.body, valor_x)
    if isinstance(arbol, ast.Constant) and isinstance(arbol.value, (int, float)):
        return float(arbol.value)
    if isinstance(arbol, ast.Name):
        if arbol.id == "x":
            return valor_x
        if arbol.id == "pi":
            return PI
        if arbol.id == "e":
            return E
        raise ValueError(f"Variable no permitida: {arbol.id}")
    if isinstance(arbol, ast.UnaryOp) and isinstance(arbol.op, (ast.USub, ast.UAdd)):
        valor = _evaluar_arbol(arbol.operand, valor_x)
        return -valor if isinstance(arbol.op, ast.USub) else valor
    if isinstance(arbol, ast.BinOp):
        izquierda = _evaluar_arbol(arbol.left, valor_x)
        derecha = _evaluar_arbol(arbol.right, valor_x)
        if isinstance(arbol.op, ast.Add):
            return izquierda + derecha
        if isinstance(arbol.op, ast.Sub):
            return izquierda - derecha
        if isinstance(arbol.op, ast.Mult):
            return izquierda * derecha
        if isinstance(arbol.op, ast.Div):
            if derecha == 0:
                raise ZeroDivisionError
            return izquierda / derecha
        if isinstance(arbol.op, ast.Pow):
            return izquierda ** derecha
    if isinstance(arbol, ast.Call) and isinstance(arbol.func, ast.Name):
        if arbol.func.id not in FUNCIONES or len(arbol.args) != 1 or arbol.keywords:
            raise ValueError("Funcion o cantidad de argumentos no permitida.")
        return FUNCIONES[arbol.func.id](_evaluar_arbol(arbol.args[0], valor_x))
    raise ValueError("La expresion contiene elementos no permitidos.")


def _crear_evaluador(funcion_str):
    arbol = ast.parse(funcion_str.replace("^", "**"), mode="eval")
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Attribute, ast.List, ast.Dict, ast.Set, ast.Compare)):
            raise ValueError("La expresion contiene elementos no permitidos.")
    return lambda valor_x: _evaluar_arbol(arbol, valor_x)


PUNTOS_INFINITO = {
    "inf": math.inf, "+inf": math.inf, "infinito": math.inf, "+infinito": math.inf,
    "oo": math.inf, "+oo": math.inf, "∞": math.inf, "+∞": math.inf,
    "-inf": -math.inf, "-infinito": -math.inf, "-oo": -math.inf, "-∞": -math.inf,
}
PASOS_APROXIMACION = 12
UMBRAL_DIVERGENCIA = 1e6
CRECIMIENTO_DIVERGENCIA = 10
TOLERANCIA_ESTABLE = 1e-6
TOLERANCIA_LATERALES = 1e-5

_registro = logging.getLogger("heyalgb.limites")


def _interpretar_punto(punto_str):
    """Convierte el punto ingresado en float; admite ±inf y expresiones como pi/2."""
    texto = punto_str.strip().lower().replace(" ", "")
    if not texto:
        raise ValueError("Ingrese el punto al que tiende x.")
    if texto in PUNTOS_INFINITO:
        return PUNTOS_INFINITO[texto]
    from core.metodos_numericos.biseccion import _crear_funcion

    try:
        return _crear_funcion(punto_str)(0.0)
    except ValueError as error:
        raise ValueError(
            f"El punto «{punto_str}» no es válido: use un número, una expresión "
            "como pi/2, o inf / -inf."
        ) from error


def _evaluar_en(evaluador, x):
    """Evalúa un punto; devuelve None si f no está definida y ±inf si desborda."""
    try:
        valor = evaluador(x)
    except OverflowError:
        return math.inf
    except (ValueError, ArithmeticError):
        return None
    if isinstance(valor, complex):
        return None
    valor = float(valor)
    if math.isnan(valor):
        return None
    return valor


def _cercanos(a, b, tolerancia):
    return abs(a - b) <= tolerancia * max(1.0, abs(a), abs(b))


def _clasificar_tendencia(valores):
    """Describe cómo se comportan f(x_k) al acercarse al punto.

    Devuelve (tipo, valor) con tipo en: "valor", "+inf", "-inf",
    "indefinida" o "inestable".
    """
    # Los últimos puntos pueden quedar fuera del dominio por la tolerancia de
    # las funciones (tan cerca de pi/2): se analiza el tramo definido previo.
    valores = list(valores)
    while valores and valores[-1] is None:
        valores.pop()
    cola = valores[-3:]
    if len(cola) < 3 or any(valor is None for valor in cola):
        return "indefinida", None
    if math.isinf(cola[-1]):
        return ("+inf" if cola[-1] > 0 else "-inf"), None
    mismo_signo = all(v > 0 for v in cola) or all(v < 0 for v in cola)
    crece = all(abs(cola[i + 1]) > abs(cola[i]) for i in range(len(cola) - 1))
    if (
        mismo_signo
        and crece
        and abs(cola[-1]) >= UMBRAL_DIVERGENCIA
        and abs(cola[-1]) >= CRECIMIENTO_DIVERGENCIA * abs(cola[0])
    ):
        return ("+inf" if cola[-1] > 0 else "-inf"), None

    # Se busca el primer tramo estable y se recorre mientras siga estable: así
    # se aprovechan los puntos más cercanos antes de que la cancelación numérica
    # (por ejemplo, 1 - cos(x) con x muy pequeño) arruine la estimación.
    for i in range(2, len(valores)):
        a, b, c = valores[i - 2], valores[i - 1], valores[i]
        if None in (a, b, c) or any(math.isinf(v) for v in (a, b, c)):
            continue
        if _cercanos(b, c, TOLERANCIA_ESTABLE) and _cercanos(a, b, 1e-3):
            ultimo = c
            for siguiente in valores[i + 1:]:
                if (
                    siguiente is None
                    or math.isinf(siguiente)
                    or not _cercanos(ultimo, siguiente, TOLERANCIA_ESTABLE)
                ):
                    break
                ultimo = siguiente
            return "valor", ultimo

    # Convergencia lenta pero geométrica (por ejemplo sqrt(x) cuando x -> 0+):
    # las diferencias tienen el mismo signo y se reducen con razón casi
    # constante. Se extrapola con el proceso Δ² de Aitken.
    ultimos = valores[-4:]
    if len(ultimos) == 4 and not any(v is None or math.isinf(v) for v in ultimos):
        d1, d2, d3 = (ultimos[i + 1] - ultimos[i] for i in range(3))
        if d1 and d2 and d3 and (d1 > 0) == (d2 > 0) == (d3 > 0):
            r1, r2 = d2 / d1, d3 / d2
            if (
                0 < r1 < 0.9
                and 0 < r2 < 0.9
                and abs(r1 - r2) <= 0.1
                and abs(d3) <= 1e-2 * max(1.0, abs(ultimos[-1]))
            ):
                return "valor", ultimos[-1] + d3 * r2 / (1 - r2)
    return "inestable", None


def _aproximaciones(evaluador, punto, signo):
    """Genera los pares (x, f(x)) que se acercan al punto por un lado."""
    if math.isinf(punto):
        xs = [math.copysign(10.0 ** k, punto) for k in range(1, PASOS_APROXIMACION + 1)]
    else:
        escala = max(1.0, abs(punto))
        xs = [
            punto + signo * escala * 10.0 ** (-k)
            for k in range(1, PASOS_APROXIMACION + 1)
        ]
    return [(x, _evaluar_en(evaluador, x)) for x in xs]


def _formatear_numero(valor):
    if valor is None:
        return "no definida"
    if math.isinf(valor):
        return "∞" if valor > 0 else "-∞"
    return f"{valor:.10g}"


def _formatear_limite(valor):
    if abs(valor) < 1e-12:
        return "0"
    texto = f"{valor:.6g}"
    if abs(valor) < 1e-6:
        return f"{texto} (muy cercano a 0; el límite podría ser 0)"
    return texto


def _describir(tendencia):
    tipo, valor = tendencia
    if tipo == "valor":
        return f"≈ {_formatear_limite(valor)}"
    if tipo == "+inf":
        return "crece sin cota (+∞)"
    if tipo == "-inf":
        return "decrece sin cota (-∞)"
    if tipo == "indefinida":
        return "f(x) no está definida cerca del punto por este lado"
    return "no se estabiliza (oscila o cambia demasiado lento para estimarlo)"


def _tabla(pares, titulo):
    lineas = [f"  Aproximación {titulo}:", f"    {'x':>22}   {'f(x)':>18}"]
    for x, valor in pares:
        lineas.append(f"    {x:>22.12g}   {_formatear_numero(valor):>18}")
    return lineas


def _resultado_lateral(tendencia):
    tipo, valor = tendencia
    if tipo == "valor":
        return f"lím f(x) ≈ {_formatear_limite(valor)}"
    if tipo in ("+inf", "-inf"):
        simbolo = "+∞" if tipo == "+inf" else "-∞"
        return f"lím f(x) = {simbolo} (diverge; el límite no es un número real)"
    return f"No se pudo determinar el límite: {_describir(tendencia)}."


def _combinar_laterales(izquierda, derecha):
    """Decide el límite bilateral a partir de los dos laterales."""
    tipo_i, valor_i = izquierda
    tipo_d, valor_d = derecha
    if tipo_i == tipo_d == "valor":
        if _cercanos(valor_i, valor_d, TOLERANCIA_LATERALES):
            return _resultado_lateral(("valor", (valor_i + valor_d) / 2))
        return (
            "El límite NO existe: los límites laterales son distintos "
            f"(izquierda ≈ {_formatear_limite(valor_i)}, "
            f"derecha ≈ {_formatear_limite(valor_d)})."
        )
    if tipo_i == tipo_d and tipo_i in ("+inf", "-inf"):
        return _resultado_lateral(izquierda)
    if {tipo_i, tipo_d} <= {"valor", "+inf", "-inf"}:
        return (
            "El límite NO existe: los límites laterales son distintos "
            f"(por la izquierda {_describir(izquierda)}; "
            f"por la derecha {_describir(derecha)})."
        )
    return (
        "El límite NO existe o no se pudo determinar: "
        f"por la izquierda {_describir(izquierda)}; "
        f"por la derecha {_describir(derecha)}."
    )


def calcular_limite(funcion_str, punto_str, direccion="bilateral"):
    """Estima un límite mediante evaluaciones cada vez más cercanas al punto.

    Es una estimación numérica: se informa la tendencia observada (valor,
    divergencia, laterales distintos o comportamiento indeterminado) sin
    presentarla como demostración.
    """
    if direccion not in ("bilateral", "izquierda", "derecha"):
        return "ERROR: Dirección no reconocida; use bilateral, izquierda o derecha."
    try:
        from core.metodos_numericos.biseccion import _crear_funcion
        from core.metodos_numericos.expresiones import normalizar_expresion

        # Misma validación segura del AST que Métodos Numéricos (nombres,
        # operadores, exponentes y complejidad). La evaluación no rechaza
        # valores grandes: son justo los que revelan una divergencia.
        _crear_funcion(funcion_str)
        evaluador = _crear_evaluador(normalizar_expresion(funcion_str))
        punto = _interpretar_punto(punto_str)
    except ValueError as error:
        return f"ERROR: {error}"

    try:
        es_infinito = math.isinf(punto)
        salida = [
            "=========================================",
            "   ANÁLISIS NUMÉRICO DE LÍMITE",
            "=========================================",
            f"Función     : f(x) = {funcion_str}",
            f"Punto       : x → {_formatear_numero(punto)}",
            "Dirección   : "
            + ("no aplica (x tiende a infinito)" if es_infinito else direccion.capitalize()),
            "-----------------------------------------",
        ]

        if es_infinito:
            pares = _aproximaciones(evaluador, punto, 1)
            salida.extend(_tabla(pares, "x → " + _formatear_numero(punto)))
            tendencia = _clasificar_tendencia([valor for _, valor in pares])
            salida.append(f"  Tendencia: {_describir(tendencia)}")
            resultado = _resultado_lateral(tendencia)
        else:
            valor_en_punto = _evaluar_en(evaluador, punto)
            linea_punto = f"f({punto:.10g}) = {_formatear_numero(valor_en_punto)}"
            if valor_en_punto is None:
                linea_punto += " (el límite puede existir aunque f no esté definida ahí)"
            salida.append(linea_punto)
            tendencias = {}
            for lado, signo, titulo in (
                ("izquierda", -1, "por la izquierda (x → c⁻)"),
                ("derecha", 1, "por la derecha (x → c⁺)"),
            ):
                if direccion not in ("bilateral", lado):
                    continue
                pares = _aproximaciones(evaluador, punto, signo)
                salida.append("")
                salida.extend(_tabla(pares, titulo))
                tendencias[lado] = _clasificar_tendencia([valor for _, valor in pares])
                salida.append(f"  Tendencia: {_describir(tendencias[lado])}")

            if direccion == "bilateral":
                resultado = _combinar_laterales(
                    tendencias["izquierda"], tendencias["derecha"]
                )
            else:
                resultado = _resultado_lateral(tendencias[direccion])

        salida.extend([
            "-----------------------------------------",
            f"[>] RESULTADO (estimación numérica): {resultado}",
            "Nota: se evaluó f(x) en puntos cada vez más cercanos; es una "
            "estimación numérica, no una demostración.",
        ])
        return "\n".join(salida)
    except Exception:
        _registro.exception(
            "Fallo inesperado al calcular el límite de %r en %r", funcion_str, punto_str
        )
        return (
            "ERROR: Ocurrió un problema inesperado al calcular el límite. "
            "Revise la expresión e inténtelo de nuevo."
        )

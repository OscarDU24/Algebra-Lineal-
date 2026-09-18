"""Calculo numerico de limites usando unicamente Python estandar."""

import ast

PI = 3.141592653589793
E = 2.718281828459045
TOLERANCIA = 1e-7


def _valor_absoluto(valor):
    return valor if valor >= 0 else -valor


def _reducir_angulo(valor):
    while valor > PI:
        valor -= 2 * PI
    while valor < -PI:
        valor += 2 * PI
    return valor


def _seno(valor):
    valor = _reducir_angulo(valor)
    termino = valor
    resultado = valor
    for indice in range(1, 18):
        termino *= -valor * valor / ((2 * indice) * (2 * indice + 1))
        resultado += termino
    return resultado


def _coseno(valor):
    valor = _reducir_angulo(valor)
    termino = 1.0
    resultado = 1.0
    for indice in range(1, 18):
        termino *= -valor * valor / ((2 * indice - 1) * (2 * indice))
        resultado += termino
    return resultado


def _raiz_cuadrada(valor):
    if valor < 0:
        raise ValueError("La raiz cuadrada requiere un valor no negativo.")
    if valor == 0:
        return 0.0
    aproximacion = valor if valor >= 1 else 1.0
    for _ in range(30):
        aproximacion = (aproximacion + valor / aproximacion) / 2
    return aproximacion


def _exponencial(valor):
    if valor < 0:
        return 1 / _exponencial(-valor)
    resultado = 1.0
    termino = 1.0
    for indice in range(1, 60):
        termino *= valor / indice
        resultado += termino
        if _valor_absoluto(termino) < 1e-15:
            break
    return resultado


def _logaritmo(valor):
    if valor <= 0:
        raise ValueError("El logaritmo requiere un valor positivo.")
    exponente = 0
    while valor > 2:
        valor /= E
        exponente += 1
    while valor < 0.5:
        valor *= E
        exponente -= 1
    z = (valor - 1) / (valor + 1)
    termino = z
    resultado = 0.0
    for indice in range(1, 80, 2):
        resultado += termino / indice
        termino *= z * z
    return 2 * resultado + exponente


def _tangente(valor):
    coseno = _coseno(valor)
    if _valor_absoluto(coseno) < TOLERANCIA:
        raise ValueError("La tangente no esta definida en este punto.")
    return _seno(valor) / coseno


FUNCIONES = {
    "sin": _seno,
    "sen": _seno,
    "cos": _coseno,
    "tan": _tangente,
    "tg": _tangente,
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


def _aproximar_limite(evaluar, punto, direccion):
    if punto == float("inf") or punto == float("-inf"):
        signo = 1 if punto > 0 else -1
        valores = [signo * (10 ** indice) for indice in range(1, 7)]
        resultados = [evaluar(valor) for valor in valores]
        return resultados[-1], resultados

    pasos = [10 ** (-indice) for indice in range(1, 8)]

    def aproximar(signo):
        resultados = [evaluar(punto + signo * paso) for paso in pasos]
        return resultados[-1], resultados

    if direccion == "izquierda":
        return aproximar(-1)
    if direccion == "derecha":
        return aproximar(1)

    izquierda, valores_izquierda = aproximar(-1)
    derecha, valores_derecha = aproximar(1)
    if _valor_absoluto(izquierda - derecha) > 1e-4:
        raise ValueError("El limite bilateral no coincide por ambos lados.")
    return (izquierda + derecha) / 2, valores_izquierda + valores_derecha


def calcular_limite(funcion_str, punto_str, direccion="bilateral"):
    """Estima un limite mediante evaluaciones cada vez mas cercanas al punto."""
    salida = [
        "=========================================",
        "   ANALISIS NUMERICO DE LIMITE",
        "=========================================",
        f"Funcion original : f(x) = {funcion_str}",
        f"Evaluando cuando : x -> {punto_str}",
        f"Direccion        : {direccion.capitalize()}",
        "-----------------------------------------",
    ]

    try:
        evaluar = _crear_evaluador(funcion_str)
        punto_limpio = punto_str.lower().strip()
        if punto_limpio in ("inf", "infinito", "oo"):
            punto = float("inf")
        elif punto_limpio in ("-inf", "-infinito", "-oo"):
            punto = float("-inf")
        else:
            punto = float(punto_limpio)

        resultado, valores = _aproximar_limite(evaluar, punto, direccion)
        salida.append("Aproximaciones sucesivas:")
        salida.append("  " + ", ".join(f"{valor:.2f}" for valor in valores[-4:]))
        salida.append(f"\n[>] RESULTADO APROXIMADO: {resultado:.2f}")
        return "\n".join(salida)
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "ERROR: Expresion invalida o limite no definido. Revisa la sintaxis y el dominio."
    except Exception as error:
        return f"ERROR INTERNO durante el calculo:\n{error}"

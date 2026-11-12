"""Normalización de notación algebraica para el evaluador AST seguro."""

import io
import tokenize


_SUPERINDICES = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁺": "+",
    "⁻": "-",
    "⁽": "(",
    "⁾": ")",
    "ᵡ": "x",
    "ᵉ": "e",
    "˙": ".",
}
_FUNCIONES = {
    "abs",
    "cos",
    "cot",
    "cotan",
    "cotangente",
    "cotg",
    "cosec",
    "cosecante",
    "csc",
    "exp",
    "ln",
    "log",
    "raiz",
    "sin",
    "sen",
    "sec",
    "secante",
    "sqrt",
    "tan",
    "tg",
}
_CONSTANTES = {"e", "pi", "x"}


def normalizar_expresion(expresion):
    """Convierte notación algebraica usual a sintaxis Python explícita."""
    if not isinstance(expresion, str):
        raise ValueError("La función debe ser texto.")

    texto = (
        expresion.replace("×", "*")
        .replace("·", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("π", "pi")
        .replace("√(", "sqrt(")
    )
    texto = _normalizar_superindices(texto)
    try:
        tokens = [
            token
            for token in tokenize.generate_tokens(io.StringIO(texto).readline)
            if token.type
            not in {
                tokenize.ENDMARKER,
                tokenize.NEWLINE,
                tokenize.NL,
                tokenize.INDENT,
                tokenize.DEDENT,
            }
        ]
    except (tokenize.TokenError, IndentationError) as error:
        raise ValueError("La expresión tiene una estructura incompleta.") from error

    normalizados = []
    anterior = None
    for token in tokens:
        tipo, valor = token.type, token.string
        if valor == "^":
            valor = "**"
            tipo = tokenize.OP
            token = tokenize.TokenInfo(
                tipo, valor, token.start, token.end, token.line
            )

        if anterior is not None and _requiere_multiplicacion(anterior, token):
            normalizados.append((tokenize.OP, "*"))
        normalizados.append((tipo, valor))
        anterior = token

    try:
        return tokenize.untokenize(normalizados)
    except (ValueError, tokenize.TokenError) as error:
        raise ValueError("No se pudo interpretar la expresión algebraica.") from error


def _normalizar_superindices(texto):
    salida = []
    indice = 0
    while indice < len(texto):
        if texto[indice] not in _SUPERINDICES:
            salida.append(texto[indice])
            indice += 1
            continue

        exponente = []
        while indice < len(texto) and texto[indice] in _SUPERINDICES:
            exponente.append(_SUPERINDICES[texto[indice]])
            indice += 1
        salida.extend(("^(", "".join(exponente), ")"))
    return "".join(salida)


def _requiere_multiplicacion(anterior, actual):
    termina_valor = (
        anterior.type == tokenize.NUMBER
        or anterior.string == ")"
        or (
            anterior.type == tokenize.NAME
            and anterior.string in _CONSTANTES
        )
    )
    inicia_valor = (
        actual.type in {tokenize.NUMBER, tokenize.NAME}
        or actual.string == "("
    )
    llamada_funcion = (
        anterior.type == tokenize.NAME
        and anterior.string in _FUNCIONES
        and actual.string == "("
    )
    return termina_valor and inicia_valor and not llamada_funcion

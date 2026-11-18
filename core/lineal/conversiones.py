from fractions import Fraction

"""
        XXXXXXXXXXXX
      XX::::::::::::XX
    XX::::::::::::::::XX        Código escrito por Charly
    XX::::::::::::::::XX         - kdcar15@github.com -
  XXXXXX::        ::XXXXXX
  XXXX  XXXXXXXXXXXX  XXXX
XX  XX                XX  XX
XX        XX    XX        XX
  XXXX    XX    XX   XXXXX
  XXXXXX    ::::    XXXXXX
XX    XXXXXXXXXXXXXXXX    XX
XX    XXXXXXXXXXXXXXXX    XX
  XXXXXX::::XXXX::::XXXXXX
    XX::XXXX::::XXXX::XXX
    XX::::::XXXX::::::XXX                       (C) 2025
      XXXXXX    XXXXXX
"""

def convertir_a_decimal(entrada):
    # Parsear el valor
    entrada = entrada.strip()
    try:
        # Tratar de convertir a fraccion
        return float(Fraction(entrada))
    except (ValueError, ZeroDivisionError):
        # En caso de no poder hacerlo, tratar de convertir
        # a decimal
        try:
            return float(entrada)
        except ValueError:
            # En caso de no poder, se dice que la entrada no
            # es un decimal ni una fraccion. Ergo, invalida.
            return None

def convertir_a_racional(entrada):
    """Convierte texto como '3', '-0.25', '1/3' o '1e-3' a Fraction exacta.

    Devuelve None si el texto no es un número racional válido (incluye
    denominador cero, 'inf' y 'nan').
    """
    try:
        return Fraction(entrada.strip())
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def convertir_a_fraccion(entrada):
    """Representa un número como fracción sin aproximarlo.

    Un Fraction se muestra tal cual. Un float se muestra con la fracción del
    decimal que Python imprime para él (0.0004 -> 1/2500), en lugar de buscar
    una fracción "cercana" que podría ocultar el valor real.
    """
    if isinstance(entrada, str):
        try:
            entrada = float(entrada)
        except ValueError:
            return str(entrada)

    if isinstance(entrada, float):
        fraccion = Fraction(repr(entrada))
    else:
        fraccion = Fraction(entrada)

    if fraccion.denominator == 1:
        return f"{fraccion.numerator}"

    return f"{fraccion.numerator}/{fraccion.denominator}"


def formatear_decimal(valor, decimales=6):
    """Muestra un número en decimal sin convertir en 0 valores pequeños no nulos."""
    numero = float(valor)
    texto = f"{numero:.{decimales}f}".rstrip("0").rstrip(".")
    if texto in ("", "-0"):
        texto = "0"
    if texto == "0" and valor != 0:
        # El redondeo ocultaría el valor: se usa notación científica.
        return f"{numero:.4g}"
    return texto

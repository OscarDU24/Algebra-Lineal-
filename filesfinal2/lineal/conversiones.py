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
    except ValueError:
        # En caso de no poder hacerlo, tratar de convertir
        # a decimal
        try:
            return float(entrada)
        except ValueError:
            # En caso de no poder, se dice que la entrada no
            # es un decimal ni una fraccion. Ergo, invalida.
            return None

def convertir_a_fraccion(entrada):
    
    numerador, denominador = entrada.as_integer_ratio()
    if(denominador == 1):
        return f"{numerador}"
    
    return f"{numerador}/{denominador}".rstrip("/1")


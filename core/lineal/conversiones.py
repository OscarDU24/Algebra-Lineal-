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
    # Asegurarnos de que sea un número flotante si viene como otro tipo
    if isinstance(entrada, str):
        try:
            entrada = float(entrada)
        except ValueError:
            return str(entrada)
            
    # Convertimos a fracción limitando el denominador para evitar números gigantes
    fraccion = Fraction(entrada).limit_denominator(1000)
    
    if fraccion.denominator == 1:
        return f"{fraccion.numerator}"
    
    return f"{fraccion.numerator}/{fraccion.denominator}"


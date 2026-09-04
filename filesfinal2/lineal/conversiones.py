from fractions import Fraction

# Codigo escrito por Charly B)
# kdcar15@github.com

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
    return f"{numerador}/{denominador}"

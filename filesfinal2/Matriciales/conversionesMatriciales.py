from fractions import Fraction


# ============================================================
# CONVERSION DE ENTRADA A DECIMAL
# ============================================================

def convertir_a_decimal(entrada):
    """
    Convierte una entrada textual a un numero decimal.

    Acepta:
        - Enteros
        - Decimales
        - Fracciones

    Retorna:
        float si la conversion es correcta.
        None si la entrada no es valida.
    """

    entrada = entrada.strip()

    try:
        return float(Fraction(entrada))

    except ValueError:

        try:
            return float(entrada)

        except ValueError:
            return None


# ============================================================
# CONVERSION DE DECIMAL A FRACCION
# ============================================================

def convertir_a_fraccion(valor):
    """
    Convierte un numero decimal a una representacion
    en forma de fraccion.
    """

    numerador, denominador = valor.as_integer_ratio()

    if denominador == 1:
        return f"{numerador}"

    return f"{numerador}/{denominador}"


# ============================================================
# CONVERSION DE MATRIZ A FRACCIONES
# ============================================================

def convertir_matriz_a_fracciones(matriz):
    """
    Convierte todos los valores de una matriz a texto
    en forma de fraccion.
    """

    resultado = []

    for fila in matriz:

        nueva_fila = []

        for valor in fila:
            nueva_fila.append(
                convertir_a_fraccion(valor)
            )

        resultado.append(nueva_fila)

    return resultado


# ============================================================
# CONVERSION DE VECTOR A FRACCIONES
# ============================================================

def convertir_vector_a_fracciones(vector):
    """
    Convierte todos los componentes de un vector
    a texto en forma de fraccion.
    """

    resultado = []

    for valor in vector:
        resultado.append(
            convertir_a_fraccion(valor)
        )

    return resultado
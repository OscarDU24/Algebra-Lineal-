from fractions import Fraction


"""
        XXXXXXXXXXXX
      XX::::::::::::XX
    XX::::::::::::::::XX
    XX::::::::::::::::XX
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
    XX::::::XXXX::::::XXX
      XXXXXX    XXXXXX
"""


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


def convertir_a_fraccion(entrada):
    """
    Convierte un numero decimal a una representacion
    en forma de fraccion.
    """

    numerador, denominador = entrada.as_integer_ratio()

    if denominador == 1:
        return f"{numerador}"

    return f"{numerador}/{denominador}".rstrip("/1")


def convertir_vector_a_fracciones(vector):
    """
    Convierte todos los componentes de un vector
    a representacion textual de fracciones.
    """

    return [
        convertir_a_fraccion(valor)
        for valor in vector
    ]


def convertir_vector_a_decimales(vector):
    """
    Convierte todos los componentes de un vector
    a valores decimales.
    """

    return [
        float(valor)
        for valor in vector
    ]
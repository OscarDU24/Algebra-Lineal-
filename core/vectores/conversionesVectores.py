from fractions import Fraction


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

    except (ValueError, ZeroDivisionError):

        try:
            return float(entrada)

        except ValueError:

            return None


def convertir_a_fraccion(entrada):
    """
    Convierte un numero decimal a una representacion
    en forma de fraccion.
    """

    fraccion = Fraction(str(entrada)).limit_denominator()

    return str(fraccion)


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
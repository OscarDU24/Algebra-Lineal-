# ============================================================
# CONVERSIONES MATRICIALES
# ============================================================

from fractions import Fraction


# ============================================================
# CONVERTIR A DECIMAL
# ============================================================

def convertir_a_decimal(entrada):

    entrada = str(
        entrada
    ).strip()

    try:

        return float(
            Fraction(entrada)
        )

    except (
        ValueError,
        ZeroDivisionError
    ):

        try:

            return float(
                entrada
            )

        except ValueError:

            return None


# ============================================================
# CONVERTIR A FRACCION
# ============================================================

def convertir_a_fraccion(valor):

    fraccion = Fraction(
        valor
    ).limit_denominator(
        10000
    )

    if fraccion.denominator == 1:

        return str(
            fraccion.numerator
        )

    return (
        f"{fraccion.numerator}/"
        f"{fraccion.denominator}"
    )


# ============================================================
# MATRIZ A FRACCIONES
# ============================================================

def convertir_matriz_a_fracciones(
    matriz
):

    resultado = []

    for fila in matriz:

        nueva_fila = []

        for valor in fila:

            nueva_fila.append(
                convertir_a_fraccion(
                    valor
                )
            )

        resultado.append(
            nueva_fila
        )

    return resultado


# ============================================================
# VECTOR A FRACCIONES
# ============================================================

def convertir_vector_a_fracciones(
    vector
):

    resultado = []

    for valor in vector:

        resultado.append(
            convertir_a_fraccion(
                valor
            )
        )

    return resultado


# =============================================================
# VARIOS VECTORES A FRACCIONES
# =============================================================

def convertir_vectores_a_fracciones(
    vectores
):

    resultado = []

    for vector in vectores:

        resultado.append(
            convertir_vector_a_fracciones(
                vector
            )
        )

    return resultado
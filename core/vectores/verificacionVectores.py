TOLERANCIA_VERIFICACION = 1e-5


def verificar_vectores(
    vector_original,
    vector_resultado,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Comprueba que dos vectores sean equivalentes
    dentro de una tolerancia numérica.
    """

    if len(vector_original) != len(vector_resultado):

        return False

    for i in range(len(vector_original)):

        if abs(
            vector_original[i]
            - vector_resultado[i]
        ) > tolerancia:

            return False

    return True


def verificar_suma(
    vector_u,
    vector_v,
    resultado,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Verifica que resultado sea correctamente
    igual a u + v.
    """

    for i in range(len(vector_u)):

        esperado = (
            vector_u[i]
            + vector_v[i]
        )

        if abs(
            esperado - resultado[i]
        ) > tolerancia:

            return False

    return True


def verificar_resta(
    vector_u,
    vector_v,
    resultado,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Verifica que resultado sea correctamente
    igual a u - v.
    """

    for i in range(len(vector_u)):

        esperado = (
            vector_u[i]
            - vector_v[i]
        )

        if abs(
            esperado - resultado[i]
        ) > tolerancia:

            return False

    return True


def verificar_multiplicacion_escalar(
    vector,
    escalar,
    resultado,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Verifica que el resultado corresponda
    a la multiplicacion del vector por un escalar.
    """

    for i in range(len(vector)):

        esperado = (
            vector[i] * escalar
        )

        if abs(
            esperado - resultado[i]
        ) > tolerancia:

            return False

    return True

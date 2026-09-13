TOLERANCIA_VERIFICACION = 1e-5


# ============================================================
# VERIFICAR VECTOR
# ============================================================

def verificar_vector(
    vector_obtenido,
    vector_esperado,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Verifica que dos vectores sean iguales
    dentro de una tolerancia.
    """

    if len(vector_obtenido) != len(vector_esperado):
        return False

    for i in range(len(vector_obtenido)):

        if abs(
            vector_obtenido[i]
            - vector_esperado[i]
        ) > tolerancia:

            return False

    return True


# ============================================================
# VERIFICAR A*x = b
# ============================================================

def verificar_ecuacion_matricial(
    matriz,
    vector_x,
    vector_b,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Comprueba que una solucion x satisfaga:

        A*x = b
    """

    if len(matriz[0]) != len(vector_x):
        return False

    if len(matriz) != len(vector_b):
        return False

    resultado = []

    for fila in matriz:

        suma = 0.0

        for j in range(len(vector_x)):

            suma += fila[j] * vector_x[j]

        resultado.append(suma)

    return verificar_vector(
        resultado,
        vector_b,
        tolerancia
    )


# ============================================================
# VERIFICAR PROPIEDAD
# ============================================================

def verificar_propiedad(
    vector_izquierda,
    vector_derecha,
    tolerancia=TOLERANCIA_VERIFICACION
):
    """
    Verifica si dos resultados vectoriales son iguales.
    """

    return verificar_vector(
        vector_izquierda,
        vector_derecha,
        tolerancia
    )
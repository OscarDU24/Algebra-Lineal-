# ============================================================
# VERIFICACION DE MATRICES Y VECTORES
# ============================================================

TOLERANCIA = 1e-9


# ============================================================
# VERIFICAR VECTOR
# ============================================================

def verificar_vector(vector):

    return (
        vector is not None
        and len(vector) > 0
    )


# ============================================================
# VERIFICAR DIMENSIONES
# ============================================================

def verificar_dimensiones(
    matriz,
    vector
):

    if not matriz:
        return False

    if not verificar_vector(vector):
        return False

    columnas = len(matriz[0])

    return len(vector) == columnas


# ============================================================
# VERIFICAR IGUALDAD DE VECTORES
# ============================================================

def verificar_propiedad(
    izquierda,
    derecha
):

    if len(izquierda) != len(derecha):
        return False

    for i in range(len(izquierda)):

        if abs(
            izquierda[i]
            - derecha[i]
        ) > TOLERANCIA:

            return False

    return True


# ============================================================
# VERIFICAR Ax = b
# ============================================================

def verificar_resultado(
    matriz,
    vector_x,
    vector_b
):

    if not verificar_dimensiones(
        matriz,
        vector_x
    ):
        return False

    resultado = []

    for fila in matriz:

        suma = 0.0

        for j in range(len(vector_x)):

            suma += (
                fila[j]
                * vector_x[j]
            )

        resultado.append(
            suma
        )

    return verificar_propiedad(
        resultado,
        vector_b
    )
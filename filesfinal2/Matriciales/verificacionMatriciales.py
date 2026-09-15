# ============================================================
# VERIFICACION DE MATRICES Y VECTORES
# ============================================================

TOLERANCIA = 1e-9


# ============================================================
# VERIFICAR MATRIZ
# ============================================================

def verificar_matriz(matriz):

    if matriz is None or len(matriz) == 0:
        return False

    if matriz[0] is None or len(matriz[0]) == 0:
        return False

    cantidad_columnas = len(matriz[0])

    for fila in matriz:

        if fila is None:
            return False

        if len(fila) != cantidad_columnas:
            return False

    return True


# ============================================================
# VERIFICAR VECTOR
# ============================================================

def verificar_vector(vector):

    return (
        vector is not None
        and len(vector) > 0
    )


# ============================================================
# OBTENER DIMENSIONES DE UNA MATRIZ
# ============================================================

def obtener_dimensiones_matriz(matriz):

    if not verificar_matriz(matriz):
        return 0, 0

    filas = len(matriz)
    columnas = len(matriz[0])

    return filas, columnas


# ============================================================
# VERIFICAR MISMAS DIMENSIONES
# ============================================================

def verificar_mismas_dimensiones(
    matriz_a,
    matriz_b
):

    if not verificar_matriz(matriz_a):
        return False

    if not verificar_matriz(matriz_b):
        return False

    filas_a, columnas_a = (
        obtener_dimensiones_matriz(
            matriz_a
        )
    )

    filas_b, columnas_b = (
        obtener_dimensiones_matriz(
            matriz_b
        )
    )

    return (
        filas_a == filas_b
        and columnas_a == columnas_b
    )


# ============================================================
# VERIFICAR SUMA DE MATRICES
# ============================================================

def verificar_suma_matrices(
    matriz_a,
    matriz_b
):

    return verificar_mismas_dimensiones(
        matriz_a,
        matriz_b
    )


# ============================================================
# VERIFICAR RESTA DE MATRICES
# ============================================================

def verificar_resta_matrices(
    matriz_a,
    matriz_b
):

    return verificar_mismas_dimensiones(
        matriz_a,
        matriz_b
    )


# ============================================================
# VERIFICAR MATRIZ Y ESCALAR
# ============================================================

def verificar_matriz_escalar(
    matriz,
    escalar
):

    if not verificar_matriz(matriz):
        return False

    return isinstance(
        escalar,
        (int, float)
    )


# ============================================================
# VERIFICAR MULTIPLICACION DE MATRICES
# ============================================================

def verificar_multiplicacion_matrices(
    matriz_a,
    matriz_b
):

    if not verificar_matriz(matriz_a):
        return False

    if not verificar_matriz(matriz_b):
        return False

    filas_a, columnas_a = (
        obtener_dimensiones_matriz(
            matriz_a
        )
    )

    filas_b, columnas_b = (
        obtener_dimensiones_matriz(
            matriz_b
        )
    )

    return columnas_a == filas_b


# ============================================================
# DIMENSIONES DEL RESULTADO DE A x B
# ============================================================

def dimensiones_resultado_multiplicacion(
    matriz_a,
    matriz_b
):

    if not verificar_multiplicacion_matrices(
        matriz_a,
        matriz_b
    ):
        return 0, 0

    filas_a, columnas_a = (
        obtener_dimensiones_matriz(
            matriz_a
        )
    )

    filas_b, columnas_b = (
        obtener_dimensiones_matriz(
            matriz_b
        )
    )

    return filas_a, columnas_b


# ============================================================
# VERIFICAR DIMENSIONES MATRIZ-VECTOR
# ============================================================

def verificar_dimensiones_matriz_vector(
    matriz,
    vector
):

    if not verificar_matriz(matriz):
        return False

    if not verificar_vector(vector):
        return False

    filas, columnas = (
        obtener_dimensiones_matriz(
            matriz
        )
    )

    return columnas == len(vector)


# ============================================================
# VERIFICAR ECUACION MATRICIAL Ax = b
# ============================================================

def verificar_ecuacion_matricial(
    matriz,
    vector_b
):

    if not verificar_matriz(matriz):
        return False

    if not verificar_vector(vector_b):
        return False

    filas, columnas = (
        obtener_dimensiones_matriz(
            matriz
        )
    )

    return filas == len(vector_b)


# ============================================================
# VERIFICAR PROPIEDAD ENTRE VECTORES
# ============================================================

def verificar_propiedad(
    izquierda,
    derecha
):

    if not verificar_vector(izquierda):
        return False

    if not verificar_vector(derecha):
        return False

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
# VERIFICAR RESULTADO DE Ax = b
# ============================================================

def verificar_resultado(
    matriz,
    vector_x,
    vector_b
):

    if not verificar_ecuacion_matricial(
        matriz,
        vector_b
    ):
        return False

    if not verificar_dimensiones_matriz_vector(
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

        resultado.append(suma)

    return verificar_propiedad(
        resultado,
        vector_b
    )
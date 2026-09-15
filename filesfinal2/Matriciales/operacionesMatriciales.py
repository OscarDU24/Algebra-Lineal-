# ============================================================
# OPERACIONES MATRICIALES
# ============================================================

TOLERANCIA = 1e-9


# ============================================================
# VERIFICACION DE MATRIZ
# ============================================================

def verificar_matriz(matriz):
    if matriz is None or len(matriz) == 0:
        return False

    if len(matriz[0]) == 0:
        return False

    cantidad_columnas = len(matriz[0])

    for fila in matriz:
        if len(fila) != cantidad_columnas:
            return False

    return True


# ============================================================
# VERIFICACION DE VECTOR
# ============================================================

def verificar_vector(vector):
    return vector is not None and len(vector) > 0


# ============================================================
# DIMENSIONES DE MATRIZ
# ============================================================

def dimensiones_matriz(matriz):
    if not verificar_matriz(matriz):
        return 0, 0

    filas = len(matriz)
    columnas = len(matriz[0])

    return filas, columnas


# ============================================================
# VERIFICAR MATRICES CON LAS MISMAS DIMENSIONES
# ============================================================

def verificar_dimensiones_matrices(matriz_a, matriz_b):
    if not verificar_matriz(matriz_a):
        return False

    if not verificar_matriz(matriz_b):
        return False

    filas_a, columnas_a = dimensiones_matriz(matriz_a)
    filas_b, columnas_b = dimensiones_matriz(matriz_b)

    return (
        filas_a == filas_b
        and columnas_a == columnas_b
    )


# ============================================================
# SUMA DE MATRICES
# ============================================================

def sumar_matrices(matriz_a, matriz_b):
    if not verificar_dimensiones_matrices(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "Las matrices deben tener las mismas "
            "dimensiones para poder sumarse."
        )

    filas, columnas = dimensiones_matriz(
        matriz_a
    )

    resultado = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            valor = (
                matriz_a[i][j]
                + matriz_b[i][j]
            )

            fila.append(valor)

        resultado.append(fila)

    return resultado


# ============================================================
# RESTA DE MATRICES
# ============================================================

def restar_matrices(matriz_a, matriz_b):
    if not verificar_dimensiones_matrices(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "Las matrices deben tener las mismas "
            "dimensiones para poder restarse."
        )

    filas, columnas = dimensiones_matriz(
        matriz_a
    )

    resultado = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            valor = (
                matriz_a[i][j]
                - matriz_b[i][j]
            )

            fila.append(valor)

        resultado.append(fila)

    return resultado


# ============================================================
# MULTIPLICACION DE MATRIZ POR ESCALAR
# ============================================================

def multiplicar_matriz_escalar(
    matriz,
    escalar
):
    if not verificar_matriz(matriz):
        raise ValueError(
            "La matriz no es valida."
        )

    resultado = []

    for fila in matriz:
        nueva_fila = []

        for valor in fila:
            nueva_fila.append(
                valor * escalar
            )

        resultado.append(nueva_fila)

    return resultado


# ============================================================
# VERIFICAR DIMENSIONES PARA MULTIPLICACION
# ============================================================

def verificar_dimensiones_multiplicacion(
    matriz_a,
    matriz_b
):
    if not verificar_matriz(matriz_a):
        return False

    if not verificar_matriz(matriz_b):
        return False

    filas_a, columnas_a = dimensiones_matriz(
        matriz_a
    )

    filas_b, columnas_b = dimensiones_matriz(
        matriz_b
    )

    return columnas_a == filas_b


# ============================================================
# MULTIPLICACION DE MATRICES
# ============================================================

def multiplicar_matrices(
    matriz_a,
    matriz_b
):
    if not verificar_dimensiones_multiplicacion(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "No se pueden multiplicar las matrices. "
            "La cantidad de columnas de A debe ser "
            "igual a la cantidad de filas de B."
        )

    filas_a, columnas_a = dimensiones_matriz(
        matriz_a
    )

    filas_b, columnas_b = dimensiones_matriz(
        matriz_b
    )

    resultado = []

    for i in range(filas_a):
        fila_resultado = []

        for j in range(columnas_b):
            suma = 0.0

            for k in range(columnas_a):
                suma += (
                    matriz_a[i][k]
                    * matriz_b[k][j]
                )

            fila_resultado.append(suma)

        resultado.append(fila_resultado)

    return resultado


# ============================================================
# VERIFICAR MATRIZ Y VECTOR
# ============================================================

def verificar_dimensiones_matriz_vector(
    matriz,
    vector
):
    if not verificar_matriz(matriz):
        return False

    if not verificar_vector(vector):
        return False

    filas, columnas = dimensiones_matriz(
        matriz
    )

    return columnas == len(vector)


# ============================================================
# PRODUCTO MATRIZ POR VECTOR
# ============================================================

def producto_matriz_vector(
    matriz,
    vector
):
    if not verificar_dimensiones_matriz_vector(
        matriz,
        vector
    ):
        raise ValueError(
            "El vector debe tener la misma cantidad "
            "de elementos que columnas tiene la matriz."
        )

    resultado = []

    for fila in matriz:
        suma = 0.0

        for j in range(len(vector)):
            suma += (
                fila[j]
                * vector[j]
            )

        resultado.append(suma)

    return resultado


# ============================================================
# PRODUCTO MATRIZ POR VECTOR DETALLADO
# ============================================================

def producto_matriz_vector_detallado(
    matriz,
    vector
):
    resultado = producto_matriz_vector(
        matriz,
        vector
    )

    pasos = []

    for i, fila in enumerate(matriz):
        terminos = []

        for j in range(len(vector)):
            terminos.append(
                f"({fila[j]})({vector[j]})"
            )

        expresion = " + ".join(
            terminos
        )

        pasos.append(
            f"Fila {i + 1}: "
            f"{expresion} = "
            f"{resultado[i]}"
        )

    return resultado, pasos


# ============================================================
# SUMA DE VECTORES
# ============================================================

def sumar_vectores(vectores):
    if not vectores:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    dimension = len(vectores[0])

    for vector in vectores:
        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimension."
            )

    resultado = [0.0] * dimension

    for vector in vectores:
        for i in range(dimension):
            resultado[i] += vector[i]

    return resultado


# ============================================================
# RESTA DE VECTORES
# ============================================================

def restar_vectores(
    vector_u,
    vector_v
):
    if len(vector_u) != len(vector_v):
        raise ValueError(
            "Los vectores deben tener "
            "la misma dimension."
        )

    resultado = []

    for i in range(len(vector_u)):
        resultado.append(
            vector_u[i] - vector_v[i]
        )

    return resultado


# ============================================================
# VECTOR POR ESCALAR
# ============================================================

def multiplicar_vector_escalar(
    vector,
    escalar
):
    resultado = []

    for valor in vector:
        resultado.append(
            valor * escalar
        )

    return resultado


# ============================================================
# COMBINACION LINEAL
# ============================================================

def combinacion_lineal(
    vectores,
    escalares
):
    if not vectores:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    if len(vectores) != len(escalares):
        raise ValueError(
            "Debe existir un escalar por cada vector."
        )

    dimension = len(vectores[0])

    for vector in vectores:
        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimension."
            )

    resultado = [0.0] * dimension

    for i in range(len(vectores)):
        vector = vectores[i]
        escalar = escalares[i]

        for j in range(dimension):
            resultado[j] += (
                escalar * vector[j]
            )

    return resultado


# ============================================================
# MATRIZ SOBRE SUMA DE VECTORES
# ============================================================

def matriz_sobre_suma_vectores(
    matriz,
    vectores
):
    vector_suma = sumar_vectores(
        vectores
    )

    resultado = producto_matriz_vector(
        matriz,
        vector_suma
    )

    return vector_suma, resultado


# ============================================================
# PROPIEDAD DISTRIBUTIVA
# ============================================================

def propiedad_distributiva(
    matriz,
    vector_u,
    vector_v
):
    suma = sumar_vectores(
        [vector_u, vector_v]
    )

    izquierda = producto_matriz_vector(
        matriz,
        suma
    )

    au = producto_matriz_vector(
        matriz,
        vector_u
    )

    av = producto_matriz_vector(
        matriz,
        vector_v
    )

    derecha = sumar_vectores(
        [au, av]
    )

    return izquierda, derecha


# ============================================================
# PROPIEDAD DEL ESCALAR
# ============================================================

def propiedad_escalar(
    matriz,
    vector,
    escalar
):
    vector_escalado = (
        multiplicar_vector_escalar(
            vector,
            escalar
        )
    )

    izquierda = producto_matriz_vector(
        matriz,
        vector_escalado
    )

    au = producto_matriz_vector(
        matriz,
        vector
    )

    derecha = multiplicar_vector_escalar(
        au,
        escalar
    )

    return izquierda, derecha


# ============================================================
# COLUMNAS DE LA MATRIZ
# ============================================================

def obtener_columnas(matriz):
    if not verificar_matriz(matriz):
        return []

    filas, columnas = dimensiones_matriz(
        matriz
    )

    resultado = []

    for j in range(columnas):
        columna = []

        for i in range(filas):
            columna.append(
                matriz[i][j]
            )

        resultado.append(columna)

    return resultado
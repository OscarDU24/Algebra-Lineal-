# ============================================================
# OPERACIONES MATRICIALES
# ============================================================

from . import verificacionMatriciales as ver


# ============================================================
# SUMA DE MATRICES
# ============================================================

def sumar_matrices(
    matriz_a,
    matriz_b
):

    if not ver.verificar_suma_matrices(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "Las matrices deben tener las mismas "
            "dimensiones para poder sumarse."
        )

    filas, columnas = (
        ver.obtener_dimensiones_matriz(
            matriz_a
        )
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

def restar_matrices(
    matriz_a,
    matriz_b
):

    if not ver.verificar_resta_matrices(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "Las matrices deben tener las mismas "
            "dimensiones para poder restarse."
        )

    filas, columnas = (
        ver.obtener_dimensiones_matriz(
            matriz_a
        )
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

    if not ver.verificar_matriz_escalar(
        matriz,
        escalar
    ):
        raise ValueError(
            "La matriz no es valida o "
            "el escalar no es numerico."
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
# MULTIPLICACION DE MATRICES
# ============================================================

def multiplicar_matrices(
    matriz_a,
    matriz_b
):

    if not ver.verificar_multiplicacion_matrices(
        matriz_a,
        matriz_b
    ):
        raise ValueError(
            "No se pueden multiplicar las matrices. "
            "La cantidad de columnas de A debe ser "
            "igual a la cantidad de filas de B."
        )

    filas_a, columnas_a = (
        ver.obtener_dimensiones_matriz(
            matriz_a
        )
    )

    filas_b, columnas_b = (
        ver.obtener_dimensiones_matriz(
            matriz_b
        )
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

            fila_resultado.append(
                suma
            )

        resultado.append(
            fila_resultado
        )

    return resultado


# ============================================================
# TRANSPOSICION DE UNA MATRIZ
#
# Si A tiene dimensiones m x n,
# entonces A^T tendra dimensiones n x m.
#
# Las filas de A se convierten en columnas
# de la matriz transpuesta.
# ============================================================

def transponer_matriz(
    matriz
):

    if not ver.verificar_matriz(
        matriz
    ):
        raise ValueError(
            "La matriz no es valida."
        )

    filas, columnas = (
        ver.obtener_dimensiones_matriz(
            matriz
        )
    )

    resultado = []

    for j in range(columnas):

        nueva_fila = []

        for i in range(filas):

            nueva_fila.append(
                matriz[i][j]
            )

        resultado.append(
            nueva_fila
        )

    return resultado


# ============================================================
# MULTIPLICACION DE MATRIZ POR VECTOR
#
# Esta operacion permite evaluar:
#
#       Ax = b
#
# En este caso conocemos A y x.
# El resultado b se obtiene mediante el producto.
# ============================================================

def producto_matriz_vector(
    matriz,
    vector_x
):

    if not ver.verificar_dimensiones_matriz_vector(
        matriz,
        vector_x
    ):
        raise ValueError(
            "El vector x debe tener la misma cantidad "
            "de elementos que columnas tiene la matriz A."
        )

    filas, columnas = (
        ver.obtener_dimensiones_matriz(
            matriz
        )
    )

    resultado_b = []

    for i in range(filas):

        suma = 0.0

        for j in range(columnas):

            suma += (
                matriz[i][j]
                * vector_x[j]
            )

        resultado_b.append(
            suma
        )

    return resultado_b


# ============================================================
# PRODUCTO MATRIZ POR VECTOR DETALLADO
#
# Permite mostrar como se obtiene cada componente de b.
# ============================================================

def producto_matriz_vector_detallado(
    matriz,
    vector_x
):

    resultado_b = producto_matriz_vector(
        matriz,
        vector_x
    )

    pasos = []

    for i, fila in enumerate(matriz):

        terminos = []

        for j in range(len(vector_x)):

            terminos.append(
                f"({fila[j]})({vector_x[j]})"
            )

        expresion = " + ".join(
            terminos
        )

        pasos.append(
            f"Fila {i + 1}: "
            f"{expresion} = "
            f"{resultado_b[i]}"
        )

    return resultado_b, pasos


# ============================================================
# SUMA DE VECTORES
# ============================================================

def sumar_vectores(
    vectores
):

    if not vectores:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    dimension = len(
        vectores[0]
    )

    for vector in vectores:

        if len(vector) != dimension:

            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimension."
            )

    resultado = (
        [0.0] * dimension
    )

    for vector in vectores:

        for i in range(dimension):

            resultado[i] += (
                vector[i]
            )

    return resultado


# ============================================================
# RESTA DE VECTORES
# ============================================================

def restar_vectores(
    vector_u,
    vector_v
):

    if not ver.verificar_vector(
        vector_u
    ):

        raise ValueError(
            "El vector u no es valido."
        )

    if not ver.verificar_vector(
        vector_v
    ):

        raise ValueError(
            "El vector v no es valido."
        )

    if len(vector_u) != len(vector_v):

        raise ValueError(
            "Los vectores deben tener "
            "la misma dimension."
        )

    resultado = []

    for i in range(
        len(vector_u)
    ):

        resultado.append(
            vector_u[i]
            - vector_v[i]
        )

    return resultado


# ============================================================
# VECTOR POR ESCALAR
# ============================================================

def multiplicar_vector_escalar(
    vector,
    escalar
):

    if not ver.verificar_vector(
        vector
    ):

        raise ValueError(
            "El vector no es valido."
        )

    if not isinstance(
        escalar,
        (int, float)
    ):

        raise ValueError(
            "El escalar debe ser numerico."
        )

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

    if len(vectores) != len(
        escalares
    ):

        raise ValueError(
            "Debe existir un escalar "
            "por cada vector."
        )

    dimension = len(
        vectores[0]
    )

    for vector in vectores:

        if len(vector) != dimension:

            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimension."
            )

    resultado = (
        [0.0] * dimension
    )

    for i in range(
        len(vectores)
    ):

        vector = vectores[i]
        escalar = escalares[i]

        for j in range(
            dimension
        ):

            resultado[j] += (
                escalar
                * vector[j]
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
#
# A(u + v) = Au + Av
# ============================================================

def propiedad_distributiva(
    matriz,
    vector_u,
    vector_v
):

    suma = sumar_vectores(
        [
            vector_u,
            vector_v
        ]
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
        [
            au,
            av
        ]
    )

    return izquierda, derecha


# ============================================================
# PROPIEDAD DEL ESCALAR
#
# A(cu) = c(Au)
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
# OBTENER COLUMNAS DE LA MATRIZ
# ============================================================

def obtener_columnas(
    matriz
):

    if not ver.verificar_matriz(
        matriz
    ):

        return []

    filas, columnas = (
        ver.obtener_dimensiones_matriz(
            matriz
        )
    )

    resultado = []

    for j in range(columnas):

        columna = []

        for i in range(filas):

            columna.append(
                matriz[i][j]
            )

        resultado.append(
            columna
        )

    return resultado
TOLERANCIA = 1e-9


# ============================================================
# VALIDACION DE MATRICES Y VECTORES
# ============================================================

def verificar_matriz(matriz):
    """
    Verifica que una matriz exista y que todas sus filas
    tengan la misma cantidad de columnas.
    """

    if not matriz:
        return False

    columnas = len(matriz[0])

    if columnas == 0:
        return False

    for fila in matriz:

        if len(fila) != columnas:
            return False

    return True


def verificar_dimensiones_matriz_vector(matriz, vector):
    """
    Verifica que la cantidad de columnas de la matriz
    coincida con la dimension del vector.
    """

    if not verificar_matriz(matriz):
        return False

    columnas = len(matriz[0])

    return columnas == len(vector)


# ============================================================
# PRODUCTO MATRIZ-VECTOR
# ============================================================

def producto_matriz_vector(matriz, vector):
    """
    Calcula el producto A*x utilizando la regla fila-vector.

    Cada componente del vector resultado se obtiene
    multiplicando una fila de A por el vector x.

        A*x =
        [
            fila_1 · x,
            fila_2 · x,
            ...
            fila_m · x
        ]

    Retorna:
        Vector resultado.
    """

    if not verificar_dimensiones_matriz_vector(
        matriz,
        vector
    ):
        raise ValueError(
            "La cantidad de columnas de la matriz "
            "debe coincidir con la dimension del vector."
        )

    resultado = []

    for fila in matriz:

        suma = 0.0

        for j in range(len(vector)):

            suma += fila[j] * vector[j]

        resultado.append(suma)

    return resultado


# ============================================================
# REGLA FILA-VECTOR DETALLADA
# ============================================================

def producto_matriz_vector_detallado(matriz, vector):
    """
    Calcula A*x y genera las operaciones correspondientes
    a la regla fila-vector.

    Retorna:
        resultado, pasos
    """

    if not verificar_dimensiones_matriz_vector(
        matriz,
        vector
    ):
        raise ValueError(
            "La cantidad de columnas de la matriz "
            "debe coincidir con la dimension del vector."
        )

    resultado = []
    pasos = []

    for i, fila in enumerate(matriz):

        suma = 0.0
        terminos = []

        for j in range(len(vector)):

            producto = fila[j] * vector[j]

            suma += producto

            terminos.append(
                f"({fila[j]:.4f})({vector[j]:.4f})"
            )

        resultado.append(suma)

        expresion = " + ".join(terminos)

        pasos.append(
            f"Fila {i + 1}: {expresion} = {suma:.6f}"
        )

    return resultado, pasos


# ============================================================
# OBTENER COLUMNAS DE UNA MATRIZ
# ============================================================

def obtener_columnas(matriz):
    """
    Obtiene las columnas de una matriz y las devuelve
    como una lista de vectores.

    Ejemplo:

        A =
        [1 2]
        [3 4]

    Retorna:

        [
            [1, 3],
            [2, 4]
        ]
    """

    if not verificar_matriz(matriz):
        raise ValueError(
            "La matriz no es valida."
        )

    filas = len(matriz)
    columnas = len(matriz[0])

    resultado = []

    for j in range(columnas):

        columna = []

        for i in range(filas):
            columna.append(
                matriz[i][j]
            )

        resultado.append(columna)

    return resultado


# ============================================================
# COMBINACION LINEAL DE VECTORES
# ============================================================

def combinacion_lineal(vectores, escalares):
    """
    Calcula una combinacion lineal:

        c1*v1 + c2*v2 + ... + cn*vn

    Los vectores deben tener la misma dimension.
    """

    if len(vectores) == 0:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    if len(vectores) != len(escalares):
        raise ValueError(
            "La cantidad de vectores debe coincidir "
            "con la cantidad de escalares."
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
# ECUACION VECTORIAL
# ============================================================

def resolver_ecuacion_vectorial(
    vectores,
    escalares
):
    """
    Calcula el vector resultante de una ecuacion vectorial.

        x1*a1 + x2*a2 + ... + xn*an

    Retorna el vector resultante.
    """

    return combinacion_lineal(
        vectores,
        escalares
    )


# ============================================================
# CONVERTIR ECUACION VECTORIAL A MATRIZ
# ============================================================

def vectores_a_matriz(vectores, vector_b):
    """
    Convierte una ecuacion vectorial:

        x1*a1 + x2*a2 + ... + xn*an = b

    en la matriz aumentada:

        [ a11 a12 ... a1n | b1 ]
        [ a21 a22 ... a2n | b2 ]
        [  .   .       .  | .  ]
        [ am1 am2 ... amn | bm ]
    """

    if len(vectores) == 0:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    dimension = len(vector_b)

    for vector in vectores:

        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimension que b."
            )

    matriz = []

    for i in range(dimension):

        fila = []

        for vector in vectores:
            fila.append(
                vector[i]
            )

        fila.append(
            vector_b[i]
        )

        matriz.append(fila)

    return matriz


# ============================================================
# VERIFICAR PROPIEDAD A(x + y) = Ax + Ay
# ============================================================

def verificar_distributividad_suma(
    matriz,
    vector_x,
    vector_y
):
    """
    Verifica la propiedad:

        A(x + y) = Ax + Ay
    """

    if not verificar_dimensiones_matriz_vector(
        matriz,
        vector_x
    ):
        raise ValueError(
            "Las dimensiones de A y x no coinciden."
        )

    if not verificar_dimensiones_matriz_vector(
        matriz,
        vector_y
    ):
        raise ValueError(
            "Las dimensiones de A y y no coinciden."
        )

    suma_xy = []

    for i in range(len(vector_x)):
        suma_xy.append(
            vector_x[i] + vector_y[i]
        )

    izquierda = producto_matriz_vector(
        matriz,
        suma_xy
    )

    ax = producto_matriz_vector(
        matriz,
        vector_x
    )

    ay = producto_matriz_vector(
        matriz,
        vector_y
    )

    derecha = []

    for i in range(len(ax)):
        derecha.append(
            ax[i] + ay[i]
        )

    return izquierda, derecha


# ============================================================
# VERIFICAR PROPIEDAD A(cx) = c(Ax)
# ============================================================

def verificar_homogeneidad(
    matriz,
    vector,
    escalar
):
    """
    Verifica la propiedad:

        A(cx) = c(Ax)
    """

    vector_escalado = []

    for componente in vector:

        vector_escalado.append(
            escalar * componente
        )

    izquierda = producto_matriz_vector(
        matriz,
        vector_escalado
    )

    ax = producto_matriz_vector(
        matriz,
        vector
    )

    derecha = []

    for componente in ax:

        derecha.append(
            escalar * componente
        )

    return izquierda, derecha
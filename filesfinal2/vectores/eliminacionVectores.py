TOLERANCIA = 1e-9

# ============================================================
# VALIDACION DE DIMENSIONES
# ============================================================

def verificar_dimensiones(vector_u, vector_v):
    """
    Verifica que dos vectores tengan la misma dimension.

    Retorna:
        True si las dimensiones coinciden.
        False si las dimensiones son diferentes.
    """
    return len(vector_u) == len(vector_v)


# ============================================================
# OPERACIONES BASICAS CON VECTORES
# ============================================================

def sumar_vectores(vectores):
    """
    Suma dos o mas vectores componente por componente.

    Recibe:
        Una lista que contiene los vectores que se desean sumar.

    Ejemplo:

        v1 = [1, 2]
        v2 = [3, 4]
        v3 = [5, 6]

        resultado = sumar_vectores([v1, v2, v3])

    produce:

        [9, 12]
    """

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


def restar_vectores(vectores):
    """
    Resta dos o mas vectores componente por componente.

    La operacion se realiza en el orden recibido:

        v1 - v2 - v3 - ...

    Ejemplo:

        v1 = [10, 10]
        v2 = [2, 3]
        v3 = [1, 2]

        resultado = [7, 5]
    """

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

    resultado = []

    for i in range(dimension):

        valor = vectores[0][i]

        for j in range(1, len(vectores)):

            valor -= vectores[j][i]

        resultado.append(valor)

    return resultado


def multiplicar_vector_escalar(vector, escalar):
    """
    Multiplica cada componente de un vector
    por un escalar.
    """

    resultado = []

    for componente in vector:

        resultado.append(
            componente * escalar
        )

    return resultado


def producto_punto(vector_u, vector_v):
    """
    Calcula el producto punto de dos vectores.
    """

    if not verificar_dimensiones(vector_u, vector_v):

        raise ValueError(
            "Los vectores deben tener la misma dimension."
        )

    resultado = 0.0

    for i in range(len(vector_u)):

        resultado += (
            vector_u[i] * vector_v[i]
        )

    return resultado


# ============================================================
# MAGNITUD Y NORMALIZACION
# ============================================================

def magnitud_vector(vector):
    """
    Calcula la magnitud de un vector.
    """

    suma = 0.0

    for componente in vector:

        suma += componente ** 2

    return suma ** 0.5


def normalizar_vector(vector):
    """
    Obtiene el vector unitario correspondiente.
    """

    magnitud = magnitud_vector(vector)

    if abs(magnitud) < TOLERANCIA:

        raise ValueError(
            "No se puede normalizar el vector cero."
        )

    resultado = []

    for componente in vector:

        resultado.append(
            componente / magnitud
        )

    return resultado


# ============================================================
# COMBINACION LINEAL
# ============================================================

def determinar_combinacion_lineal(vectores, vector_b):
    """
    Determina si un vector b puede expresarse como
    combinacion lineal de un conjunto de vectores.

    Se busca resolver:

        c1*v1 + c2*v2 + ... + ck*vk = b

    Retorna:

        tipo
        solucion
        matriz_aumentada

    tipo puede ser:

        "unica"
        "infinitas"
        "incompatible"
    """

    if not vectores:

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

    from lineal.eliminacion import eliminacion_por_filas

    matriz_aumentada = []

    for i in range(dimension):

        fila = []

        for vector in vectores:

            fila.append(
                vector[i]
            )

        fila.append(
            vector_b[i]
        )

        matriz_aumentada.append(
            fila
        )

    rref, pasos, pivotes = eliminacion_por_filas(
        matriz_aumentada,
        modo="gauss_jordan"
    )

    cantidad_variables = len(vectores)

    rango_a = 0

    for fila in rref:

        tiene_pivote = False

        for j in range(cantidad_variables):

            if abs(fila[j]) > TOLERANCIA:

                tiene_pivote = True
                break

        if tiene_pivote:

            rango_a += 1

    rango_aumentada = 0

    for fila in rref:

        tiene_elemento = False

        for valor in fila:

            if abs(valor) > TOLERANCIA:

                tiene_elemento = True
                break

        if tiene_elemento:

            rango_aumentada += 1

    if rango_a < rango_aumentada:

        return (
            "incompatible",
            None,
            matriz_aumentada
        )

    if rango_a == cantidad_variables:

        solucion = [0.0] * cantidad_variables

        for fila in rref:

            pivote = -1

            for j in range(cantidad_variables):

                if abs(fila[j]) > TOLERANCIA:

                    pivote = j
                    break

            if pivote != -1:

                solucion[pivote] = (
                    fila[cantidad_variables]
                )

        return (
            "unica",
            solucion,
            matriz_aumentada
        )

    return (
        "infinitas",
        None,
        matriz_aumentada
    )


# ============================================================
# MATRIZ A VECTORES
# ============================================================

def matriz_a_vectores(matriz):
    """
    Descompone una matriz en sus vectores columna.

    Ejemplo:

        [1 2]
        [3 4]

    se convierte en:

        v1 = [1, 3]
        v2 = [2, 4]
    """

    if not matriz:

        raise ValueError(
            "La matriz no puede estar vacia."
        )

    cantidad_columnas = len(matriz[0])

    for fila in matriz:

        if len(fila) != cantidad_columnas:

            raise ValueError(
                "La matriz debe tener filas "
                "con la misma cantidad de elementos."
            )

    vectores = []

    for j in range(cantidad_columnas):

        vector = []

        for i in range(len(matriz)):

            vector.append(
                matriz[i][j]
            )

        vectores.append(
            vector
        )

    return vectores


# ============================================================
# VECTORES A MATRIZ
# ============================================================

def vectores_a_matriz(vectores):
    """
    Convierte una lista de vectores columna
    nuevamente en una matriz.

    Ejemplo:

        v1 = [1, 3]
        v2 = [2, 4]

    produce:

        [1 2]
        [3 4]
    """

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

    matriz = []

    for i in range(dimension):

        fila = []

        for vector in vectores:

            fila.append(
                vector[i]
            )

        matriz.append(
            fila
        )

    return matriz


# ============================================================
# MATRIZ A ECUACION VECTORIAL
# ============================================================

def matriz_a_ecuacion_vectorial(matriz):
    """
    Convierte una matriz de coeficientes A
    en una ecuacion vectorial.

    Si:

        A = [v1 v2 ... vn]

    entonces:

        x1*v1 + x2*v2 + ... + xn*vn = b

    Esta funcion NO recibe ni interpreta una
    columna de terminos independientes.
    """

    vectores = matriz_a_vectores(matriz)

    nombres = []
    terminos = []

    for i in range(len(vectores)):

        nombre = f"v{i + 1}"

        nombres.append(
            nombre
        )

        terminos.append(
            f"x{i + 1}{nombre}"
        )

    ecuacion = (
        " + ".join(terminos)
        + " = b"
    )

    return (
        vectores,
        nombres,
        ecuacion
    )


# ============================================================
# SISTEMA DE ECUACIONES A ECUACION VECTORIAL
# ============================================================

def sistema_a_ecuacion_vectorial(matriz_aumentada):
    """
    Convierte una matriz aumentada [A | b]
    en una ecuacion vectorial.

    La ultima columna representa el vector b.

    Las columnas anteriores representan los
    vectores asociados a las variables.
    """

    if not matriz_aumentada:

        raise ValueError(
            "La matriz no puede estar vacia."
        )

    cantidad_columnas = len(
        matriz_aumentada[0]
    )

    if cantidad_columnas < 2:

        raise ValueError(
            "La matriz aumentada debe tener "
            "al menos una variable y una columna b."
        )

    for fila in matriz_aumentada:

        if len(fila) != cantidad_columnas:

            raise ValueError(
                "Todas las filas deben tener "
                "la misma cantidad de columnas."
            )

    # --------------------------------------------------------
    # SEPARAR A Y B
    # --------------------------------------------------------

    matriz_a = []
    vector_b = []

    for fila in matriz_aumentada:

        matriz_a.append(
            fila[:-1]
        )

        vector_b.append(
            fila[-1]
        )

    # --------------------------------------------------------
    # OBTENER LOS VECTORES COLUMNA DE A
    # --------------------------------------------------------

    vectores = matriz_a_vectores(
        matriz_a
    )

    nombres = []
    terminos = []

    for i in range(len(vectores)):

        nombre = f"v{i + 1}"

        nombres.append(
            nombre
        )

        terminos.append(
            f"x{i + 1}{nombre}"
        )

    ecuacion = (
        " + ".join(terminos)
        + " = b"
    )

    return (
        matriz_a,
        vectores,
        vector_b,
        nombres,
        ecuacion
    )
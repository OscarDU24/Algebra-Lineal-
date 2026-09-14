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

def sumar_vectores(vector_u, vector_v):
    """
    Suma dos vectores componente por componente.

    u + v = [u1 + v1, u2 + v2, ..., un + vn]
    """

    if not verificar_dimensiones(vector_u, vector_v):
        raise ValueError(
            "Los vectores deben tener la misma dimension."
        )

    resultado = []

    for i in range(len(vector_u)):
        resultado.append(
            vector_u[i] + vector_v[i]
        )

    return resultado


def restar_vectores(vector_u, vector_v):
    """
    Resta dos vectores componente por componente.

    u - v = [u1 - v1, u2 - v2, ..., un - vn]
    """

    if not verificar_dimensiones(vector_u, vector_v):
        raise ValueError(
            "Los vectores deben tener la misma dimension."
        )

    resultado = []

    for i in range(len(vector_u)):
        resultado.append(
            vector_u[i] - vector_v[i]
        )

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

    u · v = u1*v1 + u2*v2 + ... + un*vn
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

    ||v|| = sqrt(v1² + v2² + ... + vn²)
    """

    suma = 0.0

    for componente in vector:
        suma += componente ** 2

    return suma ** 0.5


def normalizar_vector(vector):
    """
    Obtiene el vector unitario correspondiente.

    vector unitario = vector / ||vector||
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
# CONVERSION DE ECUACIONES VECTORIALES A MATRIZ
# ============================================================

def vectores_a_matriz(vectores, vector_resultado):
    """
    Convierte una ecuacion vectorial en una matriz aumentada.

    Ejemplo:

        x1*u + x2*v = w

    donde:

        u = [u1, u2, u3]
        v = [v1, v2, v3]
        w = [w1, w2, w3]

    se convierte en:

        [u1  v1 | w1]
        [u2  v2 | w2]
        [u3  v3 | w3]

    Los vectores recibidos representan los vectores
    que tienen asociados los escalares x1, x2, ..., xn.
    """

    if len(vectores) == 0:
        raise ValueError(
            "Debe existir al menos un vector."
        )

    dimension = len(vector_resultado)

    for vector in vectores:
        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener la misma dimension."
            )

    matriz = []

    for i in range(dimension):
        fila = []

        for vector in vectores:
            fila.append(vector[i])

        fila.append(vector_resultado[i])

        matriz.append(fila)

    return matriz
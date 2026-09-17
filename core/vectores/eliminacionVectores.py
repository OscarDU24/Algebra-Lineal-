import math

from .constantesVectores import TOLERANCIA


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

    return [
        componente_u + componente_v
        for componente_u, componente_v in zip(vector_u, vector_v)
    ]


def restar_vectores(vector_u, vector_v):
    """
    Resta dos vectores componente por componente.

    u - v = [u1 - v1, u2 - v2, ..., un - vn]
    """

    if not verificar_dimensiones(vector_u, vector_v):
        raise ValueError(
            "Los vectores deben tener la misma dimension."
        )

    return [
        componente_u - componente_v
        for componente_u, componente_v in zip(vector_u, vector_v)
    ]


def multiplicar_vector_escalar(vector, escalar):
    """
    Multiplica cada componente de un vector
    por un escalar.
    """

    return [
        componente * escalar
        for componente in vector
    ]


def producto_punto(vector_u, vector_v):
    """
    Calcula el producto punto de dos vectores.

    u · v = u1*v1 + u2*v2 + ... + un*vn
    """

    if not verificar_dimensiones(vector_u, vector_v):
        raise ValueError(
            "Los vectores deben tener la misma dimension."
        )

    return sum(
        componente_u * componente_v
        for componente_u, componente_v in zip(vector_u, vector_v)
    )


# ============================================================
# MAGNITUD Y NORMALIZACION
# ============================================================

def magnitud_vector(vector):
    """
    Calcula la magnitud de un vector.

    ||v|| = sqrt(v1² + v2² + ... + vn²)
    """

    suma = sum(componente ** 2 for componente in vector)

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

    return [
        componente / magnitud
        for componente in vector
    ]


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

    return [
        [vector[i] for vector in vectores] + [vector_resultado[i]]
        for i in range(dimension)
    ]

def producto_cruz(vector_u, vector_v):
    """
    Calcula el producto cruz de dos vectores de R3.

    u x v = [u2*v3 - u3*v2,
            u3*v1 - u1*v3,
            u1*v2 - u2*v1]
    """

    if len(vector_u) != 3 or len(vector_v) != 3:
        raise ValueError("El producto cruz solo esta definido para 3 dimensiones.")

    return [
        vector_u[1] * vector_v[2] - vector_u[2] * vector_v[1],
        vector_u[2] * vector_v[0] - vector_u[0] * vector_v[2],
        vector_u[0] * vector_v[1] - vector_u[1] * vector_v[0]
    ]

def angulo_entre_vectores(vector_u, vector_v):
    """
    Calcula el angulo entre dos vectores en grados.

    cos(theta) = (u . v) / (||u|| * ||v||)
    theta = arccos(cos(theta))
    """

    dot = producto_punto(vector_u, vector_v)
    mag_u = magnitud_vector(vector_u)
    mag_v = magnitud_vector(vector_v)

    if mag_u < TOLERANCIA or mag_v < TOLERANCIA:
        raise ValueError("No se puede calcular el angulo con el vector cero.")

    cos_theta = max(-1.0, min(1.0, dot / (mag_u * mag_v)))

    return math.degrees(math.acos(cos_theta))

# ============================================================
# PROYECCIÓN Y DISTANCIA
# ============================================================

def proyeccion_vector(vector_u, vector_v):
    """
    Calcula la proyección ortogonal del vector u sobre el vector v.
    proj_v(u) = ((u · v) / ||v||²) * v
    """
    dot_uv = producto_punto(vector_u, vector_v)
    mag_v_sq = sum(componente ** 2 for componente in vector_v)

    if mag_v_sq < TOLERANCIA:
        raise ValueError("No se puede proyectar sobre el vector cero.")

    escalar = dot_uv / mag_v_sq
    return multiplicar_vector_escalar(vector_v, escalar)


def distancia_vectores(vector_u, vector_v):
    """
    Calcula la distancia euclidiana entre dos vectores.
    d(u, v) = ||u - v||
    """
    diferencia = restar_vectores(vector_u, vector_v)
    return magnitud_vector(diferencia)
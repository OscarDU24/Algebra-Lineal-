from .constantesVectores import TOLERANCIA

PI = 3.141592653589793


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

    if cos_theta == 1:
        return 0.0
    if cos_theta == -1:
        return 180.0

    seno_medio = ((1 - cos_theta) / (1 + cos_theta)) ** 0.5
    tangente_medio = seno_medio / (1 + (1 + seno_medio ** 2) ** 0.5)
    angulo_medio = 0.0
    termino = tangente_medio

    for indice in range(1, 24, 2):
        angulo_medio += termino / indice
        termino *= -tangente_medio ** 2

    angulo_radianes = 4 * angulo_medio
    return angulo_radianes * 180 / PI

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


# ============================================================
# COMBINACION LINEAL Y CONVERSIONES
# ============================================================

def determinar_combinacion_lineal(vectores, vector_b):
    """Determina si b pertenece al espacio generado por los vectores."""
    if not vectores:
        raise ValueError("Debe existir al menos un vector.")

    dimension = len(vector_b)
    if any(len(vector) != dimension for vector in vectores):
        raise ValueError("Todos los vectores deben tener la dimension de b.")

    from core.lineal.eliminacion import eliminacion_por_filas

    matriz_aumentada = [
        [vector[i] for vector in vectores] + [vector_b[i]]
        for i in range(dimension)
    ]
    rref, _, _ = eliminacion_por_filas(
        matriz_aumentada,
        modo="gauss_jordan"
    )

    cantidad_variables = len(vectores)
    rango_a = sum(
        any(abs(fila[j]) > TOLERANCIA for j in range(cantidad_variables))
        for fila in rref
    )
    rango_aumentada = sum(
        any(abs(valor) > TOLERANCIA for valor in fila)
        for fila in rref
    )

    if rango_a < rango_aumentada:
        return "incompatible", None, matriz_aumentada

    if rango_a == cantidad_variables:
        solucion = [0.0] * cantidad_variables
        for fila in rref:
            for indice in range(cantidad_variables):
                if abs(fila[indice] - 1) < TOLERANCIA:
                    solucion[indice] = fila[-1]
                    break
        return "unica", solucion, matriz_aumentada

    return "infinitas", None, matriz_aumentada


def matriz_a_vectores(matriz):
    """Descompone una matriz en sus vectores columna."""
    if not matriz or any(len(fila) != len(matriz[0]) for fila in matriz):
        raise ValueError("La matriz debe ser rectangular y no estar vacia.")

    return [
        [matriz[i][j] for i in range(len(matriz))]
        for j in range(len(matriz[0]))
    ]


def vectores_a_matriz(vectores):
    """Construye una matriz colocando los vectores como columnas."""
    if not vectores:
        raise ValueError("Debe existir al menos un vector.")

    dimension = len(vectores[0])
    if any(len(vector) != dimension for vector in vectores):
        raise ValueError("Todos los vectores deben tener la misma dimension.")

    return [
        [vector[i] for vector in vectores]
        for i in range(dimension)
    ]


def matriz_a_ecuacion_vectorial(matriz):
    """Convierte las columnas de una matriz en una ecuacion vectorial."""
    vectores = matriz_a_vectores(matriz)
    nombres = [f"v{i + 1}" for i in range(len(vectores))]
    ecuacion = " + ".join(
        f"x{i + 1}{nombre}"
        for i, nombre in enumerate(nombres)
    ) + " = b"
    return vectores, nombres, ecuacion


def sistema_a_ecuacion_vectorial(matriz_aumentada):
    """Convierte una matriz aumentada [A | b] en una ecuacion vectorial."""
    if not matriz_aumentada or any(
        len(fila) != len(matriz_aumentada[0])
        for fila in matriz_aumentada
    ):
        raise ValueError("La matriz aumentada debe ser rectangular y no estar vacia.")
    if len(matriz_aumentada[0]) < 2:
        raise ValueError("La matriz aumentada debe incluir A y el vector b.")

    matriz = [fila[:-1] for fila in matriz_aumentada]
    vector_b = [fila[-1] for fila in matriz_aumentada]
    vectores, nombres, ecuacion = matriz_a_ecuacion_vectorial(matriz)
    return matriz, vectores, vector_b, nombres, ecuacion
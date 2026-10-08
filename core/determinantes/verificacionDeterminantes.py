# ============================================================
# VERIFICACION DE DETERMINANTES
# ============================================================

TOLERANCIA = 1e-9


# ============================================================
# VERIFICAR MATRIZ
# ============================================================

def verificar_matriz(matriz):

    if matriz is None:
        return False

    if len(matriz) == 0:
        return False

    if matriz[0] is None:
        return False

    if len(matriz[0]) == 0:
        return False

    columnas = len(matriz[0])

    for fila in matriz:

        if fila is None:
            return False

        if len(fila) != columnas:
            return False

    return True


# ============================================================
# VERIFICAR MATRIZ CUADRADA
# ============================================================

def verificar_matriz_cuadrada(matriz):

    if not verificar_matriz(matriz):
        return False

    filas = len(matriz)
    columnas = len(matriz[0])

    return filas == columnas


# ============================================================
# OBTENER DIMENSIONES
# ============================================================

def obtener_dimensiones_matriz(matriz):

    if not verificar_matriz(matriz):
        return 0, 0

    return len(matriz), len(matriz[0])


# ============================================================
# OBTENER ORDEN DE LA MATRIZ
# ============================================================

def obtener_orden_matriz(matriz):

    if not verificar_matriz_cuadrada(matriz):
        return 0

    return len(matriz)


# ============================================================
# VERIFICAR MATRIZ PARA DETERMINANTE
# ============================================================

def verificar_determinante(matriz):

    if not verificar_matriz(matriz):

        raise ValueError(
            "La matriz no es valida."
        )

    if not verificar_matriz_cuadrada(matriz):

        raise ValueError(
            "No se puede calcular el determinante "
            "porque la matriz no es cuadrada."
        )

    return True


# ============================================================
# VERIFICAR SISTEMA PARA CRAMER
# ============================================================

def verificar_sistema_cramer(matriz, vector):

    verificar_determinante(matriz)

    if vector is None or len(vector) == 0:

        raise ValueError(
            "El vector de resultados no puede estar vacio."
        )

    orden = obtener_orden_matriz(matriz)

    if len(vector) != orden:

        raise ValueError(
            "El vector debe tener la misma cantidad "
            "de elementos que filas tiene la matriz."
        )

    return True
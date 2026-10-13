# ============================================================
# REGLA DE CRAMER
# ============================================================

from . import verificacionDeterminantes as ver
from . import operacionesDeterminantes as op


# ============================================================
# CREAR MATRIZ DE CRAMER
# ============================================================

def crear_matriz_cramer(
    matriz,
    vector,
    columna
):

    ver.verificar_sistema_cramer(
        matriz,
        vector
    )

    orden = len(matriz)

    if columna < 0 or columna >= orden:

        raise ValueError(
            "La columna de Cramer no existe."
        )

    resultado = []

    for i in range(orden):

        nueva_fila = []

        for j in range(orden):

            if j == columna:

                nueva_fila.append(
                    vector[i]
                )

            else:

                nueva_fila.append(
                    matriz[i][j]
                )

        resultado.append(
            nueva_fila
        )

    return resultado


# ============================================================
# CALCULAR DETERMINANTES DE CRAMER
# ============================================================

def calcular_determinantes_cramer(
    matriz,
    vector
):

    ver.verificar_sistema_cramer(
        matriz,
        vector
    )

    determinante_principal = (
        op.calcular_determinante(
            matriz
        )
    )

    orden = len(matriz)

    determinantes = []

    for columna in range(orden):

        matriz_cramer = crear_matriz_cramer(
            matriz,
            vector,
            columna
        )

        determinante = (
            op.calcular_determinante(
                matriz_cramer
            )
        )

        determinantes.append(
            determinante
        )

    return (
        determinante_principal,
        determinantes
    )


# ============================================================
# RESOLVER SISTEMA POR CRAMER
# ============================================================

def resolver_cramer(
    matriz,
    vector
):

    ver.verificar_sistema_cramer(
        matriz,
        vector
    )

    determinante_principal = (
        op.calcular_determinante(
            matriz
        )
    )

    if abs(determinante_principal) < ver.TOLERANCIA:

        raise ValueError(
            "No se puede aplicar la Regla de Cramer "
            "porque el determinante de la matriz "
            "principal es igual a cero."
        )

    orden = len(matriz)

    determinantes = []
    solucion = []

    for columna in range(orden):

        matriz_cramer = crear_matriz_cramer(
            matriz,
            vector,
            columna
        )

        determinante = (
            op.calcular_determinante(
                matriz_cramer
            )
        )

        determinantes.append(
            determinante
        )

        solucion.append(
            determinante
            / determinante_principal
        )

    return (
        determinante_principal,
        determinantes,
        solucion
    )
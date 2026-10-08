# ============================================================
# OPERACIONES DE DETERMINANTES
# ============================================================

from . import verificacionDeterminantes as ver


# ============================================================
# CONVERTIR VALOR A NUMERO
# ============================================================

def convertir_numero(valor):

    if isinstance(valor, (int, float)):

        return float(valor)

    try:

        return float(valor)

    except (ValueError, TypeError):

        raise ValueError(
            "La matriz contiene un valor que no es numerico."
        )


# ============================================================
# DETERMINANTE 1x1
# ============================================================

def determinante_1x1(matriz):

    ver.verificar_determinante(matriz)

    if len(matriz) != 1:

        raise ValueError(
            "La matriz debe ser de 1x1."
        )

    return convertir_numero(
        matriz[0][0]
    )


# ============================================================
# DETERMINANTE 2x2
# ============================================================

def determinante_2x2(matriz):

    ver.verificar_determinante(matriz)

    if len(matriz) != 2:

        raise ValueError(
            "La matriz debe ser de 2x2."
        )

    a = convertir_numero(
        matriz[0][0]
    )

    b = convertir_numero(
        matriz[0][1]
    )

    c = convertir_numero(
        matriz[1][0]
    )

    d = convertir_numero(
        matriz[1][1]
    )

    return (
        (a * d)
        - (b * c)
    )


# ============================================================
# CALCULAR DETERMINANTE 2x2 DETALLADO
# ============================================================

def determinante_2x2_detallado(matriz):

    ver.verificar_determinante(matriz)

    if len(matriz) != 2:

        raise ValueError(
            "La matriz debe ser de 2x2."
        )

    a = convertir_numero(
        matriz[0][0]
    )

    b = convertir_numero(
        matriz[0][1]
    )

    c = convertir_numero(
        matriz[1][0]
    )

    d = convertir_numero(
        matriz[1][1]
    )

    producto_1 = a * d

    producto_2 = b * c

    resultado = (
        producto_1 - producto_2
    )

    return (
        a,
        b,
        c,
        d,
        producto_1,
        producto_2,
        resultado
    )


# ============================================================
# DETERMINANTE POR REGLA DE SARRUS
# ============================================================

def determinante_sarrus(matriz):

    ver.verificar_determinante(matriz)

    if len(matriz) != 3:

        raise ValueError(
            "La matriz debe ser de 3x3."
        )

    a = convertir_numero(
        matriz[0][0]
    )

    b = convertir_numero(
        matriz[0][1]
    )

    c = convertir_numero(
        matriz[0][2]
    )

    d = convertir_numero(
        matriz[1][0]
    )

    e = convertir_numero(
        matriz[1][1]
    )

    f = convertir_numero(
        matriz[1][2]
    )

    g = convertir_numero(
        matriz[2][0]
    )

    h = convertir_numero(
        matriz[2][1]
    )

    i = convertir_numero(
        matriz[2][2]
    )

    diagonal_1 = a * e * i

    diagonal_2 = b * f * g

    diagonal_3 = c * d * h

    diagonal_4 = c * e * g

    diagonal_5 = b * d * i

    diagonal_6 = a * f * h

    positivos = (
        diagonal_1
        + diagonal_2
        + diagonal_3
    )

    negativos = (
        diagonal_4
        + diagonal_5
        + diagonal_6
    )

    resultado = (
        positivos - negativos
    )

    return (
        diagonal_1,
        diagonal_2,
        diagonal_3,
        diagonal_4,
        diagonal_5,
        diagonal_6,
        positivos,
        negativos,
        resultado
    )


# ============================================================
# OBTENER MENOR DE UNA MATRIZ
# ============================================================

def obtener_menor(
    matriz,
    fila,
    columna
):

    ver.verificar_determinante(
        matriz
    )

    orden = len(matriz)

    if fila < 0 or fila >= orden:

        raise ValueError(
            "La fila indicada no existe."
        )

    if columna < 0 or columna >= orden:

        raise ValueError(
            "La columna indicada no existe."
        )

    menor = []

    for i in range(orden):

        if i == fila:
            continue

        nueva_fila = []

        for j in range(orden):

            if j == columna:
                continue

            valor = convertir_numero(
                matriz[i][j]
            )

            nueva_fila.append(
                valor
            )

        menor.append(
            nueva_fila
        )

    return menor


# ============================================================
# CALCULAR COFACTOR
# ============================================================

def calcular_cofactor(
    matriz,
    fila,
    columna
):

    menor = obtener_menor(
        matriz,
        fila,
        columna
    )

    signo = (-1) ** (
        fila + columna
    )

    orden_menor = len(menor)

    # --------------------------------------------------------
    # MENOR 0x0
    # --------------------------------------------------------

    if orden_menor == 0:

        determinante_menor = 1

    # --------------------------------------------------------
    # MENOR 1x1
    # --------------------------------------------------------

    elif orden_menor == 1:

        determinante_menor = (
            convertir_numero(
                menor[0][0]
            )
        )

    # --------------------------------------------------------
    # MENOR 2x2
    # --------------------------------------------------------

    elif orden_menor == 2:

        determinante_menor = (
            determinante_2x2(
                menor
            )
        )

    # --------------------------------------------------------
    # MENOR 3x3 O MAYOR
    # --------------------------------------------------------

    else:

        determinante_menor = (
            determinante_cofactores(
                menor
            )
        )

    cofactor = (
        signo
        * determinante_menor
    )

    return cofactor


# ============================================================
# DETERMINANTE POR COFACTORES
# ============================================================

def determinante_cofactores(
    matriz
):

    ver.verificar_determinante(
        matriz
    )

    orden = len(matriz)

    # --------------------------------------------------------
    # MATRIZ 1x1
    # --------------------------------------------------------

    if orden == 1:

        return convertir_numero(
            matriz[0][0]
        )

    # --------------------------------------------------------
    # MATRIZ 2x2
    # --------------------------------------------------------

    if orden == 2:

        return determinante_2x2(
            matriz
        )

    # --------------------------------------------------------
    # EXPANSION POR LA PRIMERA FILA
    # --------------------------------------------------------

    resultado = 0

    for columna in range(orden):

        elemento = convertir_numero(
            matriz[0][columna]
        )

        cofactor = calcular_cofactor(
            matriz,
            0,
            columna
        )

        aporte = (
            elemento * cofactor
        )

        resultado += aporte

    return resultado


# ============================================================
# CALCULAR DETERMINANTE
# ============================================================

def calcular_determinante(
    matriz
):

    ver.verificar_determinante(
        matriz
    )

    orden = len(matriz)

    if orden == 1:

        return determinante_1x1(
            matriz
        )

    if orden == 2:

        return determinante_2x2(
            matriz
        )

    if orden == 3:

        return determinante_sarrus(
            matriz
        )

    return determinante_cofactores(
        matriz
    )
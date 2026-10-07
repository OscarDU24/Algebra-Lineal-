# ============================================================
# VISUALIZACION DE DETERMINANTES
# ============================================================

from Matriciales.conversionesMatriciales import (
    convertir_a_fraccion
)

import Determinantes.operacionesDeterminantes as op


# ============================================================
# FORMATEAR NUMERO
# ============================================================

def formatear_numero(
    valor,
    formato="Decimales"
):

    if formato == "Fracciones":

        return convertir_a_fraccion(
            valor
        )

    if abs(valor) < 1e-9:

        valor = 0

    if float(valor).is_integer():

        return str(
            int(valor)
        )

    return f"{valor:.6f}".rstrip("0").rstrip(".")


# ============================================================
# MATRIZ A STRING
# ============================================================

def matriz_a_string(
    matriz,
    formato="Decimales"
):

    filas = []

    for fila in matriz:

        valores = []

        for valor in fila:

            valores.append(
                formatear_numero(
                    valor,
                    formato
                )
            )

        filas.append(
            "[ "
            + "   ".join(valores)
            + " ]"
        )

    return "\n".join(
        filas
    )


# ============================================================
# VECTOR A STRING
# ============================================================

def vector_a_string(
    vector,
    formato="Decimales"
):

    return (
        "[ "
        + "   ".join(
            formatear_numero(
                valor,
                formato
            )
            for valor in vector
        )
        + " ]"
    )


# ============================================================
# DETERMINANTE 1x1
# ============================================================

def determinante_1x1_a_string(
    matriz,
    resultado,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Matriz de orden 1x1."
    )

    salida.append("")

    salida.append(
        "det(A) = a₁₁"
    )

    salida.append(
        "det(A) = "
        + formatear_numero(
            matriz[0][0],
            formato
        )
    )

    salida.append("")

    salida.append(
        "Resultado:"
    )

    salida.append(
        "det(A) = "
        + formatear_numero(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# DETERMINANTE GENERAL
# ============================================================

def determinante_a_string(
    matriz,
    determinante,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "det(A) = "
        + formatear_numero(
            determinante,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR DETERMINANTE 2x2
# ============================================================

def determinante_2x2_a_string(
    matriz,
    datos,
    formato="Decimales"
):

    (
        a,
        b,
        c,
        d,
        producto_1,
        producto_2,
        resultado
    ) = datos

    salida = []

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Teorema de ad - bc:"
    )

    salida.append("")

    salida.append(
        "det(A) = (a × d) - (b × c)"
    )

    salida.append(
        "det(A) = ("
        + formatear_numero(a, formato)
        + " × "
        + formatear_numero(d, formato)
        + ") - ("
        + formatear_numero(b, formato)
        + " × "
        + formatear_numero(c, formato)
        + ")"
    )

    salida.append(
        "det(A) = "
        + formatear_numero(
            producto_1,
            formato
        )
        + " - "
        + formatear_numero(
            producto_2,
            formato
        )
    )

    salida.append(
        "det(A) = "
        + formatear_numero(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR DETERMINANTE POR SARRUS
# ============================================================

def determinante_sarrus_a_string(
    matriz,
    datos,
    formato="Decimales"
):

    (
        diagonal_1,
        diagonal_2,
        diagonal_3,
        diagonal_4,
        diagonal_5,
        diagonal_6,
        positivos,
        negativos,
        resultado
    ) = datos

    salida = []

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Regla de Sarrus:"
    )

    salida.append("")

    salida.append(
        "Diagonales positivas:"
    )

    salida.append(
        formatear_numero(
            diagonal_1,
            formato
        )
        + " + "
        + formatear_numero(
            diagonal_2,
            formato
        )
        + " + "
        + formatear_numero(
            diagonal_3,
            formato
        )
        + " = "
        + formatear_numero(
            positivos,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Diagonales negativas:"
    )

    salida.append(
        formatear_numero(
            diagonal_4,
            formato
        )
        + " + "
        + formatear_numero(
            diagonal_5,
            formato
        )
        + " + "
        + formatear_numero(
            diagonal_6,
            formato
        )
        + " = "
        + formatear_numero(
            negativos,
            formato
        )
    )

    salida.append("")

    salida.append(
        "det(A) = "
        + formatear_numero(
            positivos,
            formato
        )
        + " - "
        + formatear_numero(
            negativos,
            formato
        )
    )

    salida.append(
        "det(A) = "
        + formatear_numero(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR PROCEDIMIENTO POR COFACTORES
# ============================================================

def cofactores_a_string(
    matriz,
    formato="Decimales"
):

    salida = []

    orden = len(matriz)

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Expansión por la primera fila:"
    )

    salida.append("")

    # --------------------------------------------------------
    # FORMULA DE EXPANSION
    # --------------------------------------------------------

    formula = "det(A) = "

    for columna in range(orden):

        if columna > 0:

            if columna % 2 == 0:

                formula += " + "

            else:

                formula += " - "

        formula += (
            "a₁"
            + str(columna + 1)
            + "C₁"
            + str(columna + 1)
        )

    salida.append(
        formula
    )

    salida.append("")

    aportes = []

    # --------------------------------------------------------
    # CALCULAR COFACTORES
    # --------------------------------------------------------

    for columna in range(orden):

        numero = columna + 1

        elemento = matriz[0][columna]

        signo = (
            (-1) ** columna
        )

        menor = (
            op.obtener_menor(
                matriz,
                0,
                columna
            )
        )

        cofactor = (
            op.calcular_cofactor(
                matriz,
                0,
                columna
            )
        )

        # ----------------------------------------------------
        # IDENTIFICACION
        # ----------------------------------------------------

        salida.append(
            "C₁"
            + str(numero)
            + ":"
        )

        if signo == 1:

            salida.append(
                "Signo: +"
            )

        else:

            salida.append(
                "Signo: -"
            )

        salida.append("")

        # ----------------------------------------------------
        # MENOR
        # ----------------------------------------------------

        salida.append(
            "Menor M₁"
            + str(numero)
            + ":"
        )

        salida.append(
            matriz_a_string(
                menor,
                formato
            )
        )

        salida.append("")

        # ----------------------------------------------------
        # DETERMINANTE DEL MENOR
        # ----------------------------------------------------

        if len(menor) == 1:

            determinante_menor = (
                menor[0][0]
            )

            salida.append(
                "M₁"
                + str(numero)
                + " = "
                + formatear_numero(
                    determinante_menor,
                    formato
                )
            )

        elif len(menor) == 2:

            a = menor[0][0]
            b = menor[0][1]
            c = menor[1][0]
            d = menor[1][1]

            producto_1 = a * d
            producto_2 = b * c

            determinante_menor = (
                producto_1
                - producto_2
            )

            salida.append(
                "M₁"
                + str(numero)
                + " = ("
                + formatear_numero(a, formato)
                + " × "
                + formatear_numero(d, formato)
                + ") - ("
                + formatear_numero(b, formato)
                + " × "
                + formatear_numero(c, formato)
                + ")"
            )

            salida.append(
                "M₁"
                + str(numero)
                + " = "
                + formatear_numero(
                    producto_1,
                    formato
                )
                + " - "
                + formatear_numero(
                    producto_2,
                    formato
                )
            )

            salida.append(
                "M₁"
                + str(numero)
                + " = "
                + formatear_numero(
                    determinante_menor,
                    formato
                )
            )

        else:

            determinante_menor = (
                op.determinante_cofactores(
                    menor
                )
            )

            salida.append(
                "Determinante del menor = "
                + formatear_numero(
                    determinante_menor,
                    formato
                )
            )

        salida.append("")

        # ----------------------------------------------------
        # COFACTOR
        # ----------------------------------------------------

        salida.append(
            "C₁"
            + str(numero)
            + " = ("
            + str(signo)
            + ") × "
            + formatear_numero(
                determinante_menor,
                formato
            )
        )

        salida.append(
            "C₁"
            + str(numero)
            + " = "
            + formatear_numero(
                cofactor,
                formato
            )
        )

        salida.append("")

        # ----------------------------------------------------
        # APORTE
        # ----------------------------------------------------

        aporte = (
            elemento * cofactor
        )

        aportes.append(
            aporte
        )

        salida.append(
            "Aporte:"
        )

        salida.append(
            formatear_numero(
                elemento,
                formato
            )
            + " × "
            + formatear_numero(
                cofactor,
                formato
            )
            + " = "
            + formatear_numero(
                aporte,
                formato
            )
        )

        salida.append("")

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    salida.append(
        "Resultado de la expansión:"
    )

    expresion = ""

    for i, aporte in enumerate(aportes):

        if i == 0:

            expresion += (
                formatear_numero(
                    aporte,
                    formato
                )
            )

        elif aporte >= 0:

            expresion += (
                " + "
                + formatear_numero(
                    aporte,
                    formato
                )
            )

        else:

            expresion += (
                " - "
                + formatear_numero(
                    abs(aporte),
                    formato
                )
            )

    salida.append(
        "det(A) = "
        + expresion
    )

    resultado = sum(aportes)

    salida.append(
        "det(A) = "
        + formatear_numero(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR MATRIZ DE CRAMER
# ============================================================

def matriz_cramer_a_string(
    matriz,
    vector,
    matriz_cramer,
    numero_variable,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Matriz original A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Vector b:"
    )

    salida.append(
        vector_a_string(
            vector,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Matriz A"
        + str(numero_variable)
        + ":"
    )

    salida.append(
        matriz_a_string(
            matriz_cramer,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR PROCEDIMIENTO COMPLETO DE CRAMER
# ============================================================

def procedimiento_cramer_a_string(
    matriz,
    vector,
    formato="Decimales"
):

    salida = []

    orden = len(matriz)

    salida.append(
        "REGLA DE CRAMER"
    )

    salida.append("")

    salida.append(
        "Matriz A:"
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        "Vector b:"
    )

    salida.append(
        vector_a_string(
            vector,
            formato
        )
    )

    salida.append("")

    # --------------------------------------------------------
    # DETERMINANTE PRINCIPAL
    # --------------------------------------------------------

    determinante_principal = (
        op.calcular_determinante(
            matriz
        )
    )

    salida.append(
        "Determinante principal:"
    )

    salida.append(
        "D = "
        + formatear_numero(
            determinante_principal,
            formato
        )
    )

    salida.append("")

    # --------------------------------------------------------
    # MATRICES DE CRAMER
    # --------------------------------------------------------

    determinantes = []

    for columna in range(orden):

        matriz_cramer = (
            cramer_matriz(
                matriz,
                vector,
                columna
            )
        )

        determinante = (
            op.calcular_determinante(
                matriz_cramer
            )
        )

        determinantes.append(
            determinante
        )

        letra = chr(
            ord("x") + columna
        )

        salida.append(
            "Matriz D"
            + letra
            + ":"
        )

        salida.append(
            matriz_a_string(
                matriz_cramer,
                formato
            )
        )

        salida.append("")

        salida.append(
            "D"
            + letra
            + " = "
            + formatear_numero(
                determinante,
                formato
            )
        )

        salida.append("")

    # --------------------------------------------------------
    # SOLUCIONES
    # --------------------------------------------------------

    if abs(determinante_principal) < 1e-9:

        salida.append(
            "No se puede aplicar la Regla de Cramer."
        )

        salida.append(
            "El determinante principal es igual a cero."
        )

        return "\n".join(
            salida
        )

    salida.append(
        "Soluciones:"
    )

    salida.append("")

    for i in range(orden):

        letra = chr(
            ord("x") + i
        )

        solucion = (
            determinantes[i]
            / determinante_principal
        )

        salida.append(
            letra
            + " = D"
            + letra
            + " / D"
        )

        salida.append(
            letra
            + " = "
            + formatear_numero(
                determinantes[i],
                formato
            )
            + " / "
            + formatear_numero(
                determinante_principal,
                formato
            )
        )

        salida.append(
            letra
            + " = "
            + formatear_numero(
                solucion,
                formato
            )
        )

        salida.append("")

    return "\n".join(
        salida
    )


# ============================================================
# CREAR MATRIZ DE CRAMER PARA VISUALIZACION
# ============================================================

def cramer_matriz(
    matriz,
    vector,
    columna
):

    nueva_matriz = []

    for i in range(
        len(matriz)
    ):

        nueva_fila = []

        for j in range(
            len(matriz)
        ):

            if j == columna:

                nueva_fila.append(
                    vector[i]
                )

            else:

                nueva_fila.append(
                    matriz[i][j]
                )

        nueva_matriz.append(
            nueva_fila
        )

    return nueva_matriz


# ============================================================
# MOSTRAR SOLUCION DE CRAMER
# ============================================================

def solucion_cramer_a_string(
    determinante_principal,
    determinantes,
    solucion,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Regla de Cramer"
    )

    salida.append("")

    salida.append(
        "D = "
        + formatear_numero(
            determinante_principal,
            formato
        )
    )

    salida.append("")

    for i in range(
        len(determinantes)
    ):

        letra = chr(
            ord("x") + i
        )

        salida.append(
            "D"
            + letra
            + " = "
            + formatear_numero(
                determinantes[i],
                formato
            )
        )

        salida.append(
            letra
            + " = D"
            + letra
            + " / D"
        )

        salida.append(
            letra
            + " = "
            + formatear_numero(
                determinantes[i],
                formato
            )
            + " / "
            + formatear_numero(
                determinante_principal,
                formato
            )
        )

        salida.append(
            letra
            + " = "
            + formatear_numero(
                solucion[i],
                formato
            )
        )

        salida.append("")

    return "\n".join(
        salida
    )
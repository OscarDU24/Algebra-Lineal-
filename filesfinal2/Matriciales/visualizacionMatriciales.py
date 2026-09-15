# ============================================================
# VISUALIZACION DE MATRICES Y VECTORES
# ============================================================

from .conversionesMatriciales import convertir_a_fraccion


# ============================================================
# FORMATEAR NUMERO
# ============================================================

def formatear_numero(
    valor,
    formato="Decimales"
):
    if formato == "Fracciones":
        return convertir_a_fraccion(
            float(valor)
        )

    if abs(valor) < 1e-9:
        valor = 0.0

    return f"{valor:.4f}"


# ============================================================
# MOSTRAR MATRIZ
# ============================================================

def matriz_a_string(
    matriz,
    formato="Decimales"
):
    if not matriz:
        return ""

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

    return "\n".join(filas)


# ============================================================
# MOSTRAR VECTOR
# ============================================================

def vector_a_string(
    vector,
    nombre="v",
    formato="Decimales"
):
    if not vector:
        return ""

    salida = [
        f"{nombre} =",
        "["
    ]

    for valor in vector:
        salida.append(
            "  "
            + formatear_numero(
                valor,
                formato
            )
        )

    salida.append("]")

    return "\n".join(salida)


# ============================================================
# VECTOR HORIZONTAL
# ============================================================

def vector_horizontal_a_string(
    vector,
    formato="Decimales"
):
    if not vector:
        return ""

    valores = []

    for valor in vector:
        valores.append(
            formatear_numero(
                valor,
                formato
            )
        )

    return (
        "[ "
        + ", ".join(valores)
        + " ]"
    )


# ============================================================
# MOSTRAR COLUMNAS
# ============================================================

def columnas_a_string(
    matriz,
    formato="Decimales"
):
    from .operacionesMatriciales import (
        obtener_columnas
    )

    columnas = obtener_columnas(
        matriz
    )

    salida = []

    for i, columna in enumerate(columnas):
        salida.append(
            vector_a_string(
                columna,
                f"a{i + 1}",
                formato
            )
        )

    return "\n\n".join(
        salida
    )


# ============================================================
# NOMBRE DE OPERACION CON VECTORES
# ============================================================

def nombres_suma_vectores(
    nombres
):
    return " + ".join(
        nombres
    )


# ============================================================
# ECUACION VECTORIAL
# ============================================================

def ecuacion_vectorial_a_string(
    nombres,
    escalares,
    formato="Decimales"
):
    terminos = []

    for i in range(len(nombres)):
        escalar = formatear_numero(
            escalares[i],
            formato
        )

        terminos.append(
            f"({escalar}){nombres[i]}"
        )

    return (
        " + ".join(terminos)
        + " = b"
    )


# ============================================================
# RESULTADO DE UNA OPERACION VECTORIAL
# ============================================================

def resultado_vector_a_string(
    resultado,
    nombre="b",
    formato="Decimales"
):
    return vector_a_string(
        resultado,
        nombre,
        formato
    )


# ============================================================
# RESULTADO DE UNA OPERACION MATRICIAL
# ============================================================

def resultado_matriz_a_string(
    resultado,
    nombre="Resultado",
    formato="Decimales"
):
    return (
        f"{nombre} =\n"
        + matriz_a_string(
            resultado,
            formato
        )
    )


# ============================================================
# MOSTRAR DOS MATRICES
# ============================================================

def matrices_a_string(
    matriz_a,
    matriz_b,
    formato="Decimales"
):
    salida = []

    salida.append(
        "A ="
    )

    salida.append(
        matriz_a_string(
            matriz_a,
            formato
        )
    )

    salida.append("")

    salida.append(
        "B ="
    )

    salida.append(
        matriz_a_string(
            matriz_b,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR PRODUCTO DE MATRICES
# ============================================================

def producto_matrices_a_string(
    matriz_a,
    matriz_b,
    resultado,
    formato="Decimales"
):
    salida = []

    salida.append(
        "A ="
    )

    salida.append(
        matriz_a_string(
            matriz_a,
            formato
        )
    )

    salida.append("")

    salida.append(
        "B ="
    )

    salida.append(
        matriz_a_string(
            matriz_b,
            formato
        )
    )

    salida.append("")

    salida.append(
        "A × B ="
    )

    salida.append(
        matriz_a_string(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR OPERACION MATRIZ + MATRIZ
# ============================================================

def operacion_matrices_a_string(
    matriz_a,
    matriz_b,
    resultado,
    operador="+",
    formato="Decimales"
):
    salida = []

    salida.append(
        "A ="
    )

    salida.append(
        matriz_a_string(
            matriz_a,
            formato
        )
    )

    salida.append("")

    salida.append(
        f"B ="
    )

    salida.append(
        matriz_a_string(
            matriz_b,
            formato
        )
    )

    salida.append("")

    salida.append(
        f"A {operador} B ="
    )

    salida.append(
        matriz_a_string(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR MATRIZ POR ESCALAR
# ============================================================

def matriz_escalar_a_string(
    matriz,
    escalar,
    resultado,
    formato="Decimales"
):
    salida = []

    salida.append(
        "A ="
    )

    salida.append(
        matriz_a_string(
            matriz,
            formato
        )
    )

    salida.append("")

    salida.append(
        f"c = {formatear_numero(escalar, formato)}"
    )

    salida.append("")

    salida.append(
        "cA ="
    )

    salida.append(
        matriz_a_string(
            resultado,
            formato
        )
    )

    return "\n".join(
        salida
    )
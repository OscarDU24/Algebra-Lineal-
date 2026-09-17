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

    return f"{valor:.2f}"


# ============================================================
# MOSTRAR MATRIZ
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

    return "\n".join(filas)


def matriz_escalar_a_string(
    matriz,
    escalar,
    formato="Decimales"
):
    """Muestra la matriz resultante de multiplicar A por un escalar."""

    from .operacionesMatriciales import multiplicar_matriz_escalar

    resultado = multiplicar_matriz_escalar(matriz, escalar)

    return matriz_a_string(resultado, formato)


def matriz_transpuesta_a_string(
    matriz,
    formato="Decimales"
):
    """Muestra la matriz transpuesta A^T."""

    from .operacionesMatriciales import transponer_matriz

    return matriz_a_string(transponer_matriz(matriz), formato)


# ============================================================
# MOSTRAR VECTOR
# ============================================================

def vector_a_string(
    vector,
    nombre="v",
    formato="Decimales"
):

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
# RESULTADO DE UNA OPERACION
# ============================================================

def resultado_a_string(
    resultado,
    nombre="b",
    formato="Decimales"
):

    return vector_a_string(
        resultado,
        nombre,
        formato
    )
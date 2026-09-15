# ============================================================
# VISUALIZACION DE MATRICES Y VECTORES
# ============================================================

from .conversionesMatriciales import (
    convertir_a_fraccion
)


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

    salida = []

    for fila in matriz:

        valores = []

        for valor in fila:

            valores.append(
                formatear_numero(
                    valor,
                    formato
                )
            )

        salida.append(
            "[ "
            + "   ".join(valores)
            + " ]"
        )

    return "\n".join(
        salida
    )


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

    salida = []

    if nombre:

        salida.append(
            f"{nombre} ="
        )

    salida.append("[")

    for valor in vector:

        salida.append(
            "  "
            + formatear_numero(
                valor,
                formato
            )
        )

    salida.append("]")

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR VECTOR HORIZONTAL
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
# MOSTRAR OPERACION ENTRE MATRICES
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
# MOSTRAR PRODUCTO DE MATRICES
# ============================================================

def producto_matrices_a_string(
    matriz_a,
    matriz_b,
    resultado,
    formato="Decimales"
):

    return operacion_matrices_a_string(
        matriz_a,
        matriz_b,
        resultado,
        "×",
        formato
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
        "c = "
        + formatear_numero(
            escalar,
            formato
        )
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


# ============================================================
# MOSTRAR COLUMNAS DE UNA MATRIZ
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

    if not columnas:
        return ""

    salida = []

    for i, columna in enumerate(
        columnas
    ):

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
# NOMBRES DE VECTORES EN UNA SUMA
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

    for i in range(
        len(nombres)
    ):

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
# MOSTRAR PRODUCTO MATRIZ POR VECTOR
#
# Representa:
#
#       A × x = b
#
# donde A y x son conocidos y b es el resultado.
# ============================================================

def producto_matriz_vector_a_string(
    matriz,
    vector_x,
    vector_b,
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
        "x ="
    )

    salida.append(
        vector_a_string(
            vector_x,
            "",
            formato
        )
    )

    salida.append("")

    salida.append(
        "A × x = b"
    )

    salida.append("")

    salida.append(
        "b ="
    )

    salida.append(
        vector_a_string(
            vector_b,
            "",
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR PASOS DEL PRODUCTO MATRIZ POR VECTOR
# ============================================================

def pasos_producto_matriz_vector_a_string(
    pasos
):

    if not pasos:
        return ""

    salida = [
        "Cálculo de cada componente de b:"
    ]

    salida.extend(
        pasos
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR ECUACION MATRICIAL Ax = b
#
# Representa la ecuacion antes de resolverla.
# ============================================================

def ecuacion_matricial_a_string(
    matriz,
    vector_b,
    formato="Decimales"
):

    salida = []

    salida.append(
        "ECUACION MATRICIAL"
    )

    salida.append("")

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
        "b ="
    )

    salida.append(
        vector_a_string(
            vector_b,
            "",
            formato
        )
    )

    salida.append("")

    salida.append(
        "Ax = b"
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR MATRIZ AUMENTADA
# ============================================================

def matriz_aumentada_a_string(
    matriz_aumentada,
    formato="Decimales"
):

    if not matriz_aumentada:
        return ""

    salida = []

    cantidad_columnas = (
        len(matriz_aumentada[0])
    )

    columna_resultado = (
        cantidad_columnas - 1
    )

    for fila in matriz_aumentada:

        valores = []

        for j, valor in enumerate(
            fila
        ):

            texto = formatear_numero(
                valor,
                formato
            )

            if j == columna_resultado:

                valores.append(
                    "| "
                    + texto
                )

            else:

                valores.append(
                    texto
                )

        salida.append(
            "[ "
            + "   ".join(valores)
            + " ]"
        )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR SISTEMA AUMENTADO
# ============================================================

def sistema_aumentado_a_string(
    matriz_aumentada,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Matriz aumentada [A | b]:"
    )

    salida.append("")

    salida.append(
        matriz_aumentada_a_string(
            matriz_aumentada,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR RREF
# ============================================================

def rref_a_string(
    rref,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Forma escalonada reducida (RREF):"
    )

    salida.append("")

    salida.append(
        matriz_a_string(
            rref,
            formato
        )
    )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR SOLUCION UNICA
# ============================================================

def solucion_unica_a_string(
    solucion,
    formato="Decimales"
):

    salida = []

    salida.append(
        "Solucion unica:"
    )

    salida.append("")

    for i, valor in enumerate(
        solucion
    ):

        salida.append(
            "x"
            + str(i + 1)
            + " = "
            + formatear_numero(
                valor,
                formato
            )
        )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR VARIABLES LIBRES
# ============================================================

def variables_libres_a_string(
    variables_libres
):

    if not variables_libres:

        return ""

    nombres = []

    for variable in variables_libres:

        nombres.append(
            "x"
            + str(variable + 1)
        )

    return (
        "Variables libres: "
        + ", ".join(nombres)
    )


# ============================================================
# MOSTRAR SOLUCION PARAMETRIZADA
# ============================================================

def parametrizacion_a_string(
    parametrizacion,
    formato="Decimales"
):

    if not parametrizacion:

        return ""

    expresiones, parametros = (
        parametrizacion
    )

    salida = []

    salida.append(
        "Solucion parametrizada:"
    )

    salida.append("")

    for i, expresion in enumerate(
        expresiones
    ):

        if expresion is None:

            continue

        salida.append(
            "x"
            + str(i + 1)
            + " = "
            + str(expresion)
        )

    return "\n".join(
        salida
    )


# ============================================================
# MOSTRAR SISTEMA INCOMPATIBLE
# ============================================================

def sistema_incompatible_a_string():

    return (
        "Sistema incompatible.\n\n"
        "No existe ninguna solucion."
    )


# ============================================================
# MOSTRAR CLASIFICACION DEL SISTEMA
# ============================================================

def clasificacion_sistema_a_string(
    tipo
):

    if tipo == "unica":

        return (
            "Clasificacion: "
            "sistema con solucion unica."
        )

    if tipo == "infinitas":

        return (
            "Clasificacion: "
            "sistema con infinitas soluciones."
        )

    if tipo == "incompatible":

        return (
            "Clasificacion: "
            "sistema incompatible."
        )

    return (
        "Clasificacion: desconocida."
    )


# ============================================================
# MOSTRAR RESULTADO COMPLETO DE Ax = b
# ============================================================

def solucion_ecuacion_matricial_a_string(
    informacion,
    formato="Decimales"
):

    salida = []

    tipo = informacion.get(
        "tipo"
    )

    matriz_aumentada = informacion.get(
        "matriz_aumentada"
    )

    rref = informacion.get(
        "rref"
    )

    rango_a = informacion.get(
        "rango_a"
    )

    rango_aumentada = informacion.get(
        "rango_aumentada"
    )

    salida.append(
        clasificacion_sistema_a_string(
            tipo
        )
    )

    salida.append("")

    if matriz_aumentada:

        salida.append(
            sistema_aumentado_a_string(
                matriz_aumentada,
                formato
            )
        )

        salida.append("")

    if rref:

        salida.append(
            rref_a_string(
                rref,
                formato
            )
        )

        salida.append("")

    salida.append(
        f"Rango de A: {rango_a}"
    )

    salida.append(
        f"Rango de [A | b]: "
        f"{rango_aumentada}"
    )

    salida.append("")

    if tipo == "unica":

        solucion = informacion.get(
            "solucion"
        )

        salida.append(
            solucion_unica_a_string(
                solucion,
                formato
            )
        )

    elif tipo == "infinitas":

        variables_libres = (
            informacion.get(
                "variables_libres"
            )
        )

        parametrizacion = (
            informacion.get(
                "parametrizacion"
            )
        )

        texto_libres = (
            variables_libres_a_string(
                variables_libres
            )
        )

        if texto_libres:

            salida.append(
                texto_libres
            )

            salida.append("")

        salida.append(
            parametrizacion_a_string(
                parametrizacion,
                formato
            )
        )

    elif tipo == "incompatible":

        salida.append(
            sistema_incompatible_a_string()
        )

    return "\n".join(
        salida
    )
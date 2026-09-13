# ============================================================
# COPIAR MATRIZ
# ============================================================

def copiar_matriz(matriz):
    """
    Crea una copia independiente de una matriz.
    """

    return [
        fila[:]
        for fila in matriz
    ]


# ============================================================
# COPIAR VECTOR
# ============================================================

def copiar_vector(vector):
    """
    Crea una copia independiente de un vector.
    """

    return vector[:]


# ============================================================
# MATRIZ A STRING
# ============================================================

def matriz_a_string(
    matriz,
    nombre="A"
):
    """
    Convierte una matriz a una representacion textual.
    """

    lineas = []

    lineas.append(
        f"{nombre} ="
    )

    for fila in matriz:

        valores = []

        for valor in fila:

            valores.append(
                f"{valor:9.4f}"
            )

        lineas.append(
            "| "
            + " ".join(valores)
            + " |"
        )

    return "\n".join(lineas)


# ============================================================
# MATRIZ AUMENTADA A STRING
# ============================================================

def matriz_aumentada_a_string(
    matriz,
    nombre="Matriz aumentada"
):
    """
    Convierte una matriz aumentada a texto,
    colocando una separacion antes del termino independiente.
    """

    lineas = []

    lineas.append(
        f"{nombre} ="
    )

    columnas = len(matriz[0])

    for fila in matriz:

        parte_a = []

        for j in range(columnas - 1):

            parte_a.append(
                f"{fila[j]:9.4f}"
            )

        independiente = (
            f"{fila[-1]:9.4f}"
        )

        lineas.append(
            "| "
            + " ".join(parte_a)
            + " | "
            + independiente
            + " |"
        )

    return "\n".join(lineas)


# ============================================================
# VECTOR A STRING
# ============================================================

def vector_a_string(
    vector,
    nombre="x"
):
    """
    Convierte un vector a una representacion vertical.
    """

    lineas = []

    lineas.append(
        f"{nombre} ="
    )

    for componente in vector:

        lineas.append(
            f"| {componente:9.4f} |"
        )

    return "\n".join(lineas)


# ============================================================
# PRODUCTO MATRIZ-VECTOR A STRING
# ============================================================

def producto_matriz_vector_a_string(
    matriz,
    vector,
    resultado,
    pasos
):
    """
    Genera una explicacion textual del producto A*x
    utilizando la regla fila-vector.
    """

    salida = []

    salida.append(
        "========================================================="
    )

    salida.append(
        "             PRODUCTO MATRIZ-VECTOR"
    )

    salida.append(
        "========================================================="
    )

    salida.append("")

    salida.append(
        matriz_a_string(
            matriz,
            "A"
        )
    )

    salida.append("")

    salida.append(
        vector_a_string(
            vector,
            "x"
        )
    )

    salida.append("")

    salida.append(
        "--- REGLA FILA-VECTOR ---"
    )

    for paso in pasos:

        salida.append(
            paso
        )

    salida.append("")

    salida.append(
        vector_a_string(
            resultado,
            "Ax"
        )
    )

    return "\n".join(salida)


# ============================================================
# ECUACION VECTORIAL A STRING
# ============================================================

def ecuacion_vectorial_a_string(
    vectores,
    escalares,
    vector_b
):
    """
    Genera una representacion textual de:

        x1*a1 + x2*a2 + ... + xn*an = b
    """

    terminos = []

    for i in range(len(vectores)):

        if i < len(escalares):

            escalar = escalares[i]

            terminos.append(
                f"({escalar:.4f})a{i + 1}"
            )

    izquierda = " + ".join(
        terminos
    )

    return (
        f"{izquierda} = b\n\n"
        + vector_a_string(
            vector_b,
            "b"
        )
    )


# ============================================================
# CONJUNTO SOLUCION A STRING
# ============================================================

def conjunto_solucion_a_string(
    informacion
):
    """
    Convierte la informacion del conjunto solucion
    a texto.
    """

    tipo = informacion["tipo"]

    salida = []

    salida.append(
        "--- CONJUNTO SOLUCIÓN ---"
    )

    if tipo == "incompatible":

        salida.append(
            "El sistema es incompatible."
        )

        salida.append(
            "No existe solución."
        )

        salida.append(
            "S = ∅"
        )

    elif tipo == "unica":

        solucion = informacion["solucion"]

        valores = []

        for valor in solucion:

            valores.append(
                f"{valor:.6f}"
            )

        salida.append(
            "El sistema tiene una solución única."
        )

        salida.append("")

        for i, valor in enumerate(solucion):

            salida.append(
                f"x{i + 1} = {valor:.6f}"
            )

        salida.append("")

        salida.append(
            "S = {("
            + ", ".join(valores)
            + ")}"
        )

    elif tipo == "infinitas":

        salida.append(
            "El sistema tiene infinitas soluciones."
        )

        salida.append("")

        expresiones = informacion[
            "expresiones"
        ]

        for variable in sorted(expresiones):

            salida.append(
                f"x{variable + 1} = "
                f"{expresiones[variable]}"
            )

        salida.append("")

        salida.append(
            "El conjunto solución se expresa "
            "mediante parámetros libres."
        )

    return "\n".join(salida)
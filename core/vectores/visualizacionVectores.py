from .utilidadesVectores import copiar_vector


def imprimir_vector(vector, nombre="Vector"):
    """
    Imprime un vector en formato vertical.
    """

    print(f"\n{nombre}:")

    for componente in vector:

        print(
            f"| {componente:9.2f} |"
        )


def vector_a_string(vector, nombre="Vector"):
    """
    Convierte un vector a una representacion
    textual vertical.
    """

    lineas = [
        f"{nombre}:"
    ]

    for componente in vector:

        lineas.append(
            f"| {componente:9.2f} |"
        )

    return "\n".join(lineas)


def vectores_a_string(vector_u, vector_v):
    """
    Genera una representacion textual de dos vectores.
    """

    salida = []

    salida.append(
        vector_a_string(
            vector_u,
            "Vector u"
        )
    )

    salida.append("")

    salida.append(
        vector_a_string(
            vector_v,
            "Vector v"
        )
    )

    return "\n".join(salida)
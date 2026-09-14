def leer_entero_positivo(mensaje):
    """
    Pide un numero entero estrictamente mayor que cero,
    validando la entrada.
    """

    while True:

        entrada = input(mensaje).strip()

        try:

            valor = int(entrada)

            if valor > 0:
                return valor

            print(
                "Error: el valor debe ser un entero mayor que 0."
            )

        except ValueError:

            print(
                "Error: debe ingresar un numero entero valido."
            )


def leer_flotante(mensaje):
    """
    Pide un numero real, aceptando enteros,
    decimales y negativos.
    """

    while True:

        entrada = input(mensaje).strip()

        try:

            return float(entrada)

        except ValueError:

            print(
                "Error: debe ingresar un numero valido "
                "(ej. 5, -3.2, 0.25)."
            )


def leer_dimension():
    """
    Solicita la cantidad de dimensiones del vector.
    """

    print("\n--- Dimensiones del vector ---")

    dimension = leer_entero_positivo(
        "Ingrese la cantidad de dimensiones: "
    )

    return dimension


def construir_vector(dimension, nombre="u"):
    """
    Solicita los componentes de un vector
    y construye una lista con sus valores.
    """

    print(
        f"\n--- Ingreso del vector {nombre} ---"
    )

    vector = []

    for i in range(dimension):

        componente = leer_flotante(
            f"Ingrese el componente {nombre}{i + 1}: "
        )

        vector.append(componente)

    return vector


def construir_dos_vectores(dimension):
    """
    Construye dos vectores de la misma dimension.
    """

    vector_u = construir_vector(
        dimension,
        "u"
    )

    vector_v = construir_vector(
        dimension,
        "v"
    )

    return vector_u, vector_v
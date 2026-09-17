# =============================================================
# LEER ENTERO POSITIVO
# =============================================================

def leer_entero_positivo(mensaje):
    """
    Solicita un entero estrictamente mayor que cero.
    """

    while True:

        entrada = input(
            mensaje
        ).strip()

        try:

            valor = int(
                entrada
            )

            if valor > 0:

                return valor

            print(
                "Error: el valor debe ser mayor que 0."
            )

        except ValueError:

            print(
                "Error: debe ingresar un numero entero valido."
            )


# ============================================================
# LEER NUMERO REAL
# ============================================================

def leer_flotante(mensaje):
    """
    Solicita un numero real.
    """

    while True:

        entrada = input(
            mensaje
        ).strip()

        try:

            return float(
                entrada
            )

        except ValueError:

            print(
                "Error: debe ingresar un numero valido."
            )


# ============================================================
# LEER DIMENSIONES DE A
# ============================================================

def leer_dimensiones_matriz():
    """
    Solicita las dimensiones de la matriz A.
    """

    print(
        "\n--- DIMENSIONES DE A ---"
    )

    filas = leer_entero_positivo(
        "Filas de A: "
    )

    columnas = leer_entero_positivo(
        "Columnas de A: "
    )

    return filas, columnas


# ============================================================
# CONSTRUIR MATRIZ A
# ============================================================

def construir_matriz(
    filas,
    columnas
):
    """
    Solicita los valores de A.
    """

    matriz = []

    print(
        "\n--- MATRIZ A ---"
    )

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valor = leer_flotante(
                f"A[{i + 1}][{j + 1}]: "
            )

            fila.append(
                valor
            )

        matriz.append(
            fila
        )

    return matriz


# ============================================================
# CONSTRUIR VECTOR x
# ============================================================

def construir_vector_x(
    dimension
):
    """
    Construye el vector x.

    La dimension de x es igual a la cantidad
    de columnas de A.
    """

    vector = []

    print(
        "\n--- VECTOR x ---"
    )

    for i in range(dimension):

        valor = leer_flotante(
            f"x{i + 1}: "
        )

        vector.append(
            valor
        )

    return vector


# ============================================================
# CONSTRUIR VECTOR b
# ============================================================

def construir_vector_b(
    dimension
):
    """
    Construye el vector b.

    La dimension de b es igual a la cantidad
    de filas de A.
    """

    vector = []

    print(
        "\n--- VECTOR b ---"
    )

    for i in range(dimension):

        valor = leer_flotante(
            f"b{i + 1}: "
        )

        vector.append(
            valor
        )

    return vector


# ============================================================
# CONSTRUIR VECTOR y
# ============================================================

def construir_vector_y(
    dimension
):
    """
    Construye el vector y.

    Se utiliza para propiedades como:

        A(x + y)
    """

    vector = []

    print(
        "\n--- VECTOR y ---"
    )

    for i in range(dimension):

        valor = leer_flotante(
            f"y{i + 1}: "
        )

        vector.append(
            valor
        )

    return vector
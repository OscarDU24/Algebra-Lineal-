# ============================================================
# VALIDACION DE ENTEROS POSITIVOS
# ============================================================

def leer_entero_positivo(mensaje):
    """
    Solicita un numero entero estrictamente mayor que cero.
    """

    while True:

        entrada = input(mensaje).strip()

        try:

            valor = int(entrada)

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
# VALIDACION DE NUMEROS REALES
# ============================================================

def leer_flotante(mensaje):
    """
    Solicita un numero real.
    """

    while True:

        entrada = input(mensaje).strip()

        try:
            return float(entrada)

        except ValueError:

            print(
                "Error: debe ingresar un numero valido."
            )


# ============================================================
# LEER DIMENSIONES DE UNA MATRIZ
# ============================================================

def leer_dimensiones_matriz():
    """
    Solicita la cantidad de filas y columnas.
    """

    print("\n--- Dimensiones de la matriz A ---")

    filas = leer_entero_positivo(
        "Ingrese la cantidad de filas: "
    )

    columnas = leer_entero_positivo(
        "Ingrese la cantidad de columnas: "
    )

    return filas, columnas


# ============================================================
# CONSTRUIR MATRIZ
# ============================================================

def construir_matriz(filas, columnas):
    """
    Solicita los valores de una matriz.
    """

    matriz = []

    print("\n--- Ingreso de la matriz A ---")

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valor = leer_flotante(
                f"A[{i + 1}][{j + 1}]: "
            )

            fila.append(valor)

        matriz.append(fila)

    return matriz


# ============================================================
# CONSTRUIR VECTOR
# ============================================================

def construir_vector(dimension, nombre="x"):
    """
    Solicita los componentes de un vector.
    """

    vector = []

    print(
        f"\n--- Ingreso del vector {nombre} ---"
    )

    for i in range(dimension):

        valor = leer_flotante(
            f"{nombre}{i + 1}: "
        )

        vector.append(valor)

    return vector


# ============================================================
# CONSTRUIR VECTOR B
# ============================================================

def construir_vector_b(dimension):
    """
    Construye el vector b utilizado en:

        A*x = b
    """

    return construir_vector(
        dimension,
        "b"
    )
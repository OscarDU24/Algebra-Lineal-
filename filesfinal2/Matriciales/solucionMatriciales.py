from lineal.eliminacion import eliminacion_por_filas

TOLERANCIA = 1e-9


# ============================================================
# CREAR MATRIZ AUMENTADA
# ============================================================

def crear_matriz_aumentada(matriz, vector_b):
    """
    Une A y b para formar la matriz aumentada [A | b].
    """

    if len(matriz) != len(vector_b):
        raise ValueError(
            "La cantidad de filas de A debe coincidir "
            "con la dimension de b."
        )

    aumentada = []

    for i in range(len(matriz)):

        fila = matriz[i][:]

        fila.append(
            vector_b[i]
        )

        aumentada.append(fila)

    return aumentada


# ============================================================
# CLASIFICAR SISTEMA
# ============================================================

def clasificar_sistema(matriz_aumentada):
    """
    Clasifica un sistema lineal como:

        - unica
        - infinitas
        - incompatible

    Utiliza la forma escalonada reducida.
    """

    rref, pasos, pivotes = eliminacion_por_filas(
        matriz_aumentada,
        modo="gauss_jordan"
    )

    filas = len(rref)
    columnas = len(rref[0])

    variables = columnas - 1

    # --------------------------------------------------------
    # Buscar contradicciones
    # --------------------------------------------------------

    for i in range(filas):

        todos_cero = True

        for j in range(variables):

            if abs(rref[i][j]) >= TOLERANCIA:
                todos_cero = False
                break

        termino = rref[i][-1]

        if todos_cero and abs(termino) >= TOLERANCIA:

            return {
                "tipo": "incompatible",
                "rref": rref,
                "pasos": pasos,
                "pivotes": pivotes
            }

    # --------------------------------------------------------
    # Comparar pivotes con cantidad de variables
    # --------------------------------------------------------

    cantidad_pivotes = len(pivotes)

    if cantidad_pivotes == variables:

        tipo = "unica"

    else:

        tipo = "infinitas"

    return {
        "tipo": tipo,
        "rref": rref,
        "pasos": pasos,
        "pivotes": pivotes
    }


# ============================================================
# OBTENER SOLUCION UNICA
# ============================================================

def obtener_solucion_unica(
    rref,
    cantidad_variables
):
    """
    Extrae la solucion cuando el sistema tiene
    una unica solucion.
    """

    solucion = []

    for i in range(cantidad_variables):

        solucion.append(
            rref[i][-1]
        )

    return solucion


# ============================================================
# OBTENER VARIABLES LIBRES
# ============================================================

def obtener_variables_libres(
    pivotes,
    cantidad_variables
):
    """
    Obtiene los indices correspondientes a las
    variables libres.
    """

    variables_libres = []

    for j in range(cantidad_variables):

        if j not in pivotes:

            variables_libres.append(j)

    return variables_libres


# ============================================================
# PARAMETRIZAR SOLUCION INFINITA
# ============================================================

def parametrizar_solucion(
    rref,
    pivotes,
    cantidad_variables
):
    """
    Obtiene una representacion parametrica del conjunto
    solucion cuando existen infinitas soluciones.

    Ejemplo:

        x1 = 2 - x3
        x2 = 5
        x3 = t

    """

    variables_libres = obtener_variables_libres(
        pivotes,
        cantidad_variables
    )

    parametros = {}

    for indice, variable in enumerate(
        variables_libres
    ):

        parametros[variable] = (
            f"t{indice + 1}"
        )

    expresiones = {}

    # --------------------------------------------------------
    # Asignar directamente las variables libres
    # --------------------------------------------------------

    for variable in variables_libres:

        expresiones[variable] = parametros[variable]

    # --------------------------------------------------------
    # Obtener las variables pivote
    # --------------------------------------------------------

    for fila, columna_pivote in enumerate(pivotes):

        expresion = f"{rref[fila][-1]:.6f}"

        for variable in variables_libres:

            coeficiente = rref[fila][variable]

            if abs(coeficiente) < TOLERANCIA:
                continue

            parametro = parametros[variable]

            if coeficiente > 0:

                expresion += (
                    f" - {coeficiente:.6f}"
                    f"{parametro}"
                )

            else:

                expresion += (
                    f" + {abs(coeficiente):.6f}"
                    f"{parametro}"
                )

        expresiones[columna_pivote] = expresion

    return expresiones, variables_libres


# ============================================================
# CONJUNTO SOLUCION
# ============================================================

def obtener_conjunto_solucion(
    matriz,
    vector_b
):
    """
    Analiza completamente el sistema:

        A*x = b

    y devuelve la informacion correspondiente
    al conjunto solucion.
    """

    matriz_aumentada = crear_matriz_aumentada(
        matriz,
        vector_b
    )

    informacion = clasificar_sistema(
        matriz_aumentada
    )

    tipo = informacion["tipo"]

    cantidad_variables = len(matriz[0])

    if tipo == "unica":

        solucion = obtener_solucion_unica(
            informacion["rref"],
            cantidad_variables
        )

        informacion["solucion"] = solucion

    elif tipo == "infinitas":

        expresiones, variables_libres = (
            parametrizar_solucion(
                informacion["rref"],
                informacion["pivotes"],
                cantidad_variables
            )
        )

        informacion["expresiones"] = expresiones

        informacion["variables_libres"] = (
            variables_libres
        )

    else:

        informacion["solucion"] = None

    return informacion
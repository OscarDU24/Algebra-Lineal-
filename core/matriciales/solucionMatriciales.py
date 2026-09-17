from core.lineal.eliminacion import eliminacion_por_filas

TOLERANCIA = 1e-9


def crear_matriz_aumentada(matriz, vector_b):

    if len(matriz) != len(vector_b):
        raise ValueError(
            "El vector b debe tener una componente por cada fila de A."
        )

    matriz_aumentada = []

    for i in range(len(matriz)):

        fila = list(matriz[i])

        fila.append(
            vector_b[i]
        )

        matriz_aumentada.append(fila)

    return matriz_aumentada


def clasificar_sistema(matriz_aumentada):

    rref, pasos, pivotes = eliminacion_por_filas(
        matriz_aumentada,
        modo="gauss_jordan"
    )

    filas = len(rref)
    columnas = len(rref[0])

    variables = columnas - 1

    rango_a = 0
    rango_aumentada = 0

    for fila in rref:

        tiene_coeficiente = False

        for j in range(variables):

            if abs(fila[j]) > TOLERANCIA:

                tiene_coeficiente = True
                break

        tiene_resultado = (
            abs(fila[-1]) > TOLERANCIA
        )

        if tiene_coeficiente:
            rango_a += 1

        if tiene_coeficiente or tiene_resultado:
            rango_aumentada += 1

    if rango_a < rango_aumentada:

        tipo = "incompatible"

    elif rango_a == variables:

        tipo = "unica"

    else:

        tipo = "infinitas"

    return (
        tipo,
        rref,
        pasos,
        rango_a,
        rango_aumentada
    )


def obtener_solucion_unica(rref):
    variables = len(rref[0]) - 1
    solucion = [0.0] * variables

    for fila in rref:
        for columna in range(variables):
            if abs(fila[columna] - 1) < TOLERANCIA:
                solucion[columna] = fila[-1]
                break

    return solucion


def obtener_variables_libres(rref):

    variables = len(rref[0]) - 1

    pivotes = []

    for fila in rref:

        for j in range(variables):

            if abs(fila[j] - 1) < TOLERANCIA:

                es_pivote = True

                for k in range(j):

                    if abs(fila[k]) > TOLERANCIA:

                        es_pivote = False
                        break

                if es_pivote:
                    pivotes.append(j)

                break

    libres = []

    for i in range(variables):

        if i not in pivotes:
            libres.append(i)

    return libres


def parametrizar_solucion(rref):

    variables = len(rref[0]) - 1

    libres = obtener_variables_libres(
        rref
    )

    parametros = {}

    for i, variable in enumerate(libres):

        parametros[variable] = (
            f"t{i + 1}"
        )

    expresiones = [
        None
    ] * variables

    for i in libres:

        expresiones[i] = parametros[i]

    for fila in rref:

        pivote = None

        for j in range(variables):

            if abs(
                fila[j] - 1
            ) < TOLERANCIA:

                pivote = j
                break

        if pivote is None:
            continue

        expresion = (
            str(fila[-1])
        )

        for libre in libres:

            coeficiente = fila[libre]

            if abs(coeficiente) < TOLERANCIA:
                continue

            parametro = parametros[libre]

            if coeficiente < 0:

                expresion += (
                    f" + {abs(coeficiente)}{parametro}"
                )

            else:

                expresion += (
                    f" - {coeficiente}{parametro}"
                )

        expresiones[pivote] = expresion

    return expresiones, parametros


def obtener_conjunto_solucion(
    matriz,
    vector_b
):

    matriz_aumentada = crear_matriz_aumentada(
        matriz,
        vector_b
    )

    (
        tipo,
        rref,
        pasos,
        rango_a,
        rango_aumentada
    ) = clasificar_sistema(
        matriz_aumentada
    )

    informacion = {
        "tipo": tipo,
        "rref": rref,
        "pasos": pasos,
        "rango_a": rango_a,
        "rango_aumentada": rango_aumentada,
        "variables_libres": [],
        "solucion": None,
        "parametrizacion": None
    }

    if tipo == "unica":

        informacion["solucion"] = (
            obtener_solucion_unica(
                rref
            )
        )

    elif tipo == "infinitas":

        (
            expresiones,
            parametros
        ) = parametrizar_solucion(
            rref
        )

        informacion["variables_libres"] = (
            list(parametros.keys())
        )

        informacion["parametrizacion"] = (
            expresiones,
            parametros
        )

    return informacion


def resolver_ecuacion_matricial(matriz, vector_b):
    """
    Resuelve y clasifica la ecuacion matricial A x = b.

    Devuelve la informacion de la matriz aumentada [A | b], su RREF,
    rangos, pasos de eliminacion y la solucion cuando corresponde.
    """

    return obtener_conjunto_solucion(matriz, vector_b)
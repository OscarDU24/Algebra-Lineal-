"""Motor puro de Python para tablas de intercambio de Leontief."""

from core.lineal.eliminacion import eliminacion_por_filas

TOLERANCIA = 1e-9


def _validar_matriz_cuadrada(matriz):
    if not matriz or any(len(fila) != len(matriz) for fila in matriz):
        raise ValueError("La matriz de intercambios debe ser cuadrada y no vacía.")


def _validar_vector(vector, dimension, nombre):
    if len(vector) != dimension:
        raise ValueError(f"{nombre} debe tener {dimension} componentes.")


def matriz_identidad(dimension):
    return [
        [1.0 if fila == columna else 0.0 for columna in range(dimension)]
        for fila in range(dimension)
    ]


def matriz_intercambio(entradas):
    """Construye B = I - A, donde A contiene consumos interindustriales."""
    _validar_matriz_cuadrada(entradas)
    identidad = matriz_identidad(len(entradas))
    return [
        [identidad[i][j] - entradas[i][j] for j in range(len(entradas))]
        for i in range(len(entradas))
    ]


def matriz_aumentada(matriz, demanda):
    """Construye la matriz aumentada [B | D] del sistema B X = D."""
    _validar_matriz_cuadrada(matriz)
    _validar_vector(demanda, len(matriz), "La demanda")
    return [list(fila) + [demanda[i]] for i, fila in enumerate(matriz)]


def _resolver(matriz, demanda):
    aumentada = matriz_aumentada(matriz, demanda)
    reducida, pasos, pivotes = eliminacion_por_filas(
        aumentada,
        modo="gauss_jordan"
    )

    variables = len(matriz)
    for fila in reducida:
        coeficientes_nulos = all(
            abs(fila[columna]) < TOLERANCIA
            for columna in range(variables)
        )
        if coeficientes_nulos and abs(fila[-1]) >= TOLERANCIA:
            raise ValueError("El modelo no tiene una solución compatible.")

    if len(pivotes) < variables:
        raise ValueError("El modelo tiene producción indeterminada.")

    produccion = [0.0] * variables
    for fila in reducida:
        for columna in range(variables):
            if abs(fila[columna] - 1) < TOLERANCIA:
                produccion[columna] = fila[-1]
                break

    return aumentada, reducida, pasos, produccion


def resolver_modelo_abierto(entradas, demanda):
    """Resuelve el modelo abierto X = A X + D."""
    base = matriz_intercambio(entradas)
    aumentada, reducida, pasos, produccion = _resolver(base, demanda)
    return {
        "modelo": "abierto",
        "base": base,
        "aumentada": aumentada,
        "reducida": reducida,
        "pasos": pasos,
        "produccion": produccion,
    }


def resolver_modelo_cerrado(entradas, demanda, consumo_hogares, ingreso_hogares):
    """Resuelve el modelo cerrado agregando el sector hogares como sector endógeno.

    consumo_hogares indica cuánto consume el sector hogares de cada producto.
    ingreso_hogares indica el ingreso generado por una unidad de producción de cada
    sector. La demanda externa se mantiene en los sectores productivos y es cero
    para el sector hogares.
    """
    _validar_matriz_cuadrada(entradas)
    dimension = len(entradas)
    _validar_vector(demanda, dimension, "La demanda")
    _validar_vector(consumo_hogares, dimension, "El consumo de hogares")
    _validar_vector(ingreso_hogares, dimension, "El ingreso de hogares")

    entradas_cerradas = [
        list(fila) + [consumo_hogares[i]]
        for i, fila in enumerate(entradas)
    ]
    entradas_cerradas.append(list(ingreso_hogares) + [0.0])
    demanda_cerrada = list(demanda) + [0.0]
    base = matriz_intercambio(entradas_cerradas)
    aumentada, reducida, pasos, produccion = _resolver(base, demanda_cerrada)

    return {
        "modelo": "cerrado",
        "base": base,
        "aumentada": aumentada,
        "reducida": reducida,
        "pasos": pasos,
        "produccion": produccion,
    }
